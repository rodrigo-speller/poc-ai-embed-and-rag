# %%
# Imports.

import csv
import lib.pg as pg

# %%
# Inicialização.

db = pg.connect()

with open('../data/4-CONSTITUICAO.csv', 'r', encoding="utf-8-sig") as file:
  data = list(csv.reader(file, delimiter=";"))
  data.pop(0) # remove header

# %%
# Processamento.

cur = db.cursor()

try:
  for row in data:
    cur.execute(
      """
      INSERT INTO documents.parts (id, parent_id, type, ref, text)
        VALUES (%(id)s, %(parent_id)s, %(type)s, %(ref)s, %(text)s);
      """,
      {
        "id": row[0],
        "parent_id": row[1] or None,
        "type": row[2],
        "ref": row[3],
        "text": row[4]
      }
    )

  db.commit()
except Exception as ex:
  db.rollback()
  raise ex

# %%
# Finalização.

db.close()

# %%
