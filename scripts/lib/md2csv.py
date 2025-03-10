import re

def parse_line(line):
  class LineState:
    type: str = None
    ref: str = None
    text: str = None

    def __init__(self, type: str = None, ref: str = None, text: str = None):
      self.type = type
      self.ref = ref
      self.text = text

    def __str__(self):
      return "[{}] {}: {}".format(self.type, self.ref, self.text)
    
    def __repr__(self):
      return str(self)
    
  item = LineState()
  line = line.strip()

  if line[0] == '#':
    parts = line.lstrip('# ').split(': ', 1)
    if len(parts) == 2:
      item.type = "cabecalho"
      item.ref = parts[0]
      item.text = parts[1]
    else:
      item.type = "documento"
      item.text = parts[0]

  elif line.startswith("**Art. "):
    parts = line.split('**', 2)
    item.type = "artigo"
    item.ref = parts[1].strip()
    item.text = parts[2].strip()
  elif line.startswith("**Parágrafo ") or line.startswith("**§ "):
    parts = line.split('**', 2)
    item.type = "paragrafo"
    item.ref = parts[1].strip()
    item.text = parts[2].strip()
  elif re.search("^[IVXLCDM]+ - ", line) != None:
    parts = line.split(" - ", 1)
    item.type = "inciso"
    item.ref = parts[0].strip()
    item.text = parts[1].strip()
  elif re.search("^_[a-z]\\)_", line) != None:
    parts = line.lstrip("_").split("_ ", 1)
    item.type = "alinea"
    item.ref = parts[0].strip().strip("()")
    item.text = parts[1].strip()
  elif line.startswith("**"):
    parts = line.split('**', 2)
    item.type = "texto"
    item.ref = parts[1].strip().strip(": -")
    item.text = parts[2].strip()
  else:
    item.type = "texto"
    item.text = line
  return item