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
    # Busca os documento que ainda não possuem vetor registrado.
    cursor.execute(
      """
      SELECT
        doc.id,
        documents.get_document_content(doc.id) text

        FROM documents.parts doc

        LEFT JOIN vectors.documents vec
          ON vec.doc_part_id = doc.id

        WHERE doc.type = 'artigo'
          AND vec.e5_passage_768 IS NULL

        LIMIT 10
      """
    )

    data = cursor.fetchall()
    if (len(data) < 1):
      break

    # Gera os embeddings do texto dos documentos.
    embeddings = lmodel.embed(
      text=list(map(lambda x: x[1], data)), dimensionality=768,
      prefix='passage'
    )

    for row, vec in zip(data, embeddings):
      cursor.execute(
        """
        INSERT INTO vectors.documents(doc_part_id, e5_passage_768)
          VALUES (%(doc_part_id)s, %(e5_passage_768)s)
          ON CONFLICT (doc_part_id) DO UPDATE SET e5_passage_768 = %(e5_passage_768)s
        """,
        { "doc_part_id": row[0], "e5_passage_768": vec }
      )

      db.commit()
  except Exception as ex:
    db.rollback()
    raise ex

# %%
# Finalização.

db.close()

# %%
