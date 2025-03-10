# PoC: AI Embed and RAG

## Primeiros passos

### Criar ambiente virtual do Python

```sh
python3 -m venv ./.venv
```
### Ativar ambiente virtual do Python

```sh
source .venv/bin/activate
```

### Instalar pacotes

```sh
pip install gpt4all "gpt4all[cuda]" nomic numpy psycopg2-binary
```

## Exemplos

### Exemplo simples de pesquisa semântica

- [Pesquisa semântica](./scripts/0-semantic-query-example.py)

### Exemplo de pesquisa semântica em base de dados PostgreSQL

- [Docker Compose.](./.docker/docker-compose.yml)
- [pgvector - Open-source vector similarity search for Postgres.](https://github.com/pgvector/pgvector)

#### Dados da Constituição da República Federativa do Brasil

> Origem: https://github.com/abjur/constituicao

##### Arquivos:

- **0-CONSTITUICAO.md**: Arquivo original da Constituição, conforme obtido de https://github.com/abjur/constituicao.
- **1-CONSTITUICAO.md**: Arquivo original da Constituição com pequenos ajustes e correções.
- **2-CONSTITUICAO.raw.csv**: Arquivo de dados da Constituição interpretado pelo script [1-compile-data.py](../scripts/1-compile-data.py), a partir do arquivo [1-CONSTITUICAO.md](1-CONSTITUICAO.md)
- **3-CONSTITUICAO.xlsx**: Planilha de dados da Constituição compilada manualmente, a partir da importação do arquivo [2-CONSTITUICAO.raw.csv](2-CONSTITUICAO.raw.csv)
- **4-CONSTITUICAO.csv**: Arquivo de dados da Constituição exportada do arquivo [3-CONSTITUICAO.xlsx](3-CONSTITUICAO.xlsx).

##### Scripts para criação da estrutura de banco de dados

- [Criar extensão `vector`.](./sql/extensions.sql)
- [Criar esquemas `documents` e `vectors`.](./sql/schemas.sql)
- [Criar tabela `documents.parts`.](./sql/tables/documents.parts.sql)
- [Criar tabela `vectors.parts`.](./sql/tables/vectors.parts.sql)
- [Criar tabela `vectors.documents`.](./sql/tables/vectors.documents.sql)
- [Criar tabela `vectors.questions`.](./sql/tables/vectors.questions.sql)
- [Criar função `documents.get_document_content`.](./sql/functions/documents.get_document_content.sql)
- [Criar função `documents.get_document_header_parts`.](./sql/functions/documents.get_document_header_parts.sql)
- [Criar função `documents.get_document_parts`.](./sql/functions/documents.get_document_parts.sql)
- [Comparar a similaridade entre parts de documentos.](./sql/queries/vectors_similarity.sql)
- [Realizar a pesquisa de questões em documentos.](./sql/helpers/SELECT_match_vectors.question.sql)
- [Deletar expressões de pesquisa de documentos fracos.](./sql/helpers/DELETE_weak_vectors.questions.sql)

##### Scripts para transformação de dados e população da base de dados

- [1-compile-data.py](./scripts/1-compile-data.py)
- [2-populate-db.py](./scripts/2-populate-db.py)
- [3-compute-parts-vectors.py](./scripts/3-compute-parts-vectors.py)
- [4-compute-documents-vectors.py](./scripts/4-compute-documents-vectors.py)
- [5-generate-questions.py](./scripts/5-generate-questions.py)
- [6-compute-questions-vectors.py](./scripts/6-compute-questions-vectors.py)
