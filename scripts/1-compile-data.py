# %%
# Imports.

import csv
from lib.md2csv import parse_line

# %%
# Leitura do arquivo markdown.

with open('../data/1-CONSTITUICAO.md') as file:
  lines = list(filter(None, [line.rstrip() for line in file]))

# %%
# Interpretação das linhas do arquivo.

items = list(map(parse_line, lines))

# %%
# Escrita do arquivo CSV bruto.

with open('../data/2-CONSTITUICAO.raw.csv', 'w') as file:
  writer = csv.writer(file)
  for i, item in enumerate(items):
    writer.writerow([i + 1, item.type,item.ref,item.text])
