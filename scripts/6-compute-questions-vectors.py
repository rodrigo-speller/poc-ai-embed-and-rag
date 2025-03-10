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
  cursor.execute(
    """
    SELECT
      vec.id,
      vec.question

      FROM vectors.questions vec

      WHERE vec.e5_query_768 IS NULL

      ORDER BY RANDOM()
      LIMIT 10
    """
  )

  data = cursor.fetchall()

  if (len(data) < 1):
    break

  try:
    embeddings = lmodel.embed(list(map(lambda x: x[1], data)), dimensionality=768, prefix='query')

    for row, vec in zip(data, embeddings):
      cursor.execute(
        """
        UPDATE vectors.questions SET e5_query_768 = %(e5_query_768)s
          WHERE id = %(id)s
        """,
        { "id": row[0], "e5_query_768": vec }
      )

      db.commit()
  except Exception as ex:
    db.rollback()
    raise ex

# %%
# Finalização.

db.close()

# %%
