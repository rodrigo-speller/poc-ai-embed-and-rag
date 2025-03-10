# %%
# Imports.

from gpt4all import GPT4All
import lib.pg as pg
import re

# %%
# Inicialização.

lmodel = GPT4All('Llama-3.2-1B-Instruct-Q4_0.gguf', device='cuda')
db = pg.connect()

# %%
# Processamento.

cursor = db.cursor()

while True:
  cursor.execute(
      """
      SELECT
        doc.id,
        documents.get_document_content(doc.id, true) text

        FROM documents.parts doc

        LEFT JOIN vectors.questions vec
          ON doc.id = vec.doc_part_id

        WHERE doc.type = 'artigo'
          AND vec.id IS NULL

        ORDER BY RANDOM()
        LIMIT 50
      """
  )

  data = cursor.fetchall()

  system_prompt = ' '.join(list(
      filter(
        lambda x: x,
        map(
          lambda x: x.strip(),
          """
          Você é um agente que gera as possíveis peguntas para indexação dos trechos da Consituição.
          As respostas das peguntas geradas devem estar estritamente no contexto informado.
          Não gere as respostas para as peguntas.
          As peguntas geradas devem ser diretas.
          Não deve haver erros de gramática ou ortografica nas peguntas.
          As peguntas não devem se repetir.
          """.split('\n')
        )
      )
  ))

  if (len(data) < 1):
    break

  for row in data:
    try:
      with lmodel.chat_session(system_prompt):
        answer = lmodel.generate(
              "Gere 30 perguntas considerando o seguinte contexto:\n\n" + row[1],
              temp=0.0,
              max_tokens=65535,
          )

        answer = set(
          map(
            lambda x: re.sub('^\\d+.\\s+', '', x, 0),
            filter(
              lambda x: re.match('^\\d+.\\s', x),
              map(
                lambda x: x.strip(),
                answer.split('\n')
              )
            )
          )
        )

        for question in answer:
          cursor.execute(
            """
            INSERT INTO vectors.questions(doc_part_id, question)
              VALUES (%(doc_part_id)s, %(question)s);
            """,
            { "doc_part_id": row[0], "question": question }
          )
          db.commit()

    except Exception as ex:
      db.rollback()
      raise ex

# %%
# Finalização.

db.close()

# %%
