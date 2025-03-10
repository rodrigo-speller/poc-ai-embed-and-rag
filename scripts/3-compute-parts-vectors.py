# %%
# Imports.

from gpt4all import Embed4All
import lib.pg as pg

# %%
# Inicialização.

lmodel = Embed4All('multilingual-e5-base-Q8_0.gguf', device='cuda')
db = pg.connect()

# %%
# Processamento.

cursor = db.cursor()

while True:
  try:
    cursor.execute(
      """
      SELECT part.id, part.text
        FROM documents.parts part

        LEFT JOIN vectors.parts vec
          ON vec.doc_part_id = part.id

        WHERE vec.e5_passage_768 IS NULL
          OR vec.e5_query_768 IS NULL

        LIMIT 10
      """
    )

    data = cursor.fetchall()

    if (len(data) < 1):
      break

    pembeddings = lmodel.embed(list(map(lambda x: x[1], data)), dimensionality=768, prefix='passage')
    qembeddings = lmodel.embed(list(map(lambda x: x[1], data)), dimensionality=768, prefix='query')

    for row, pvec, qvec in zip(data, pembeddings, qembeddings):
      cursor.execute(
        """
        INSERT INTO vectors.parts(doc_part_id, e5_passage_768, e5_query_768)
          VALUES (%(doc_part_id)s, %(e5_passage_768)s, %(e5_query_768)s)
          ON CONFLICT (doc_part_id) DO UPDATE SET e5_passage_768 = %(e5_passage_768)s, e5_query_768 = %(e5_query_768)s
        """,
        { "doc_part_id": row[0], "e5_passage_768": pvec, "e5_query_768": qvec }
      )

      db.commit()
  except Exception as ex:
    db.rollback()
    raise ex

# %%
# Finalização.

db.close()

# %%
