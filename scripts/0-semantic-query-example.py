# ==============================================================================
# Pesquisa semântica
# ==============================================================================
#
# Realiza uma pesquisa de similaridade semântica a partir de uma consulta
# ("query") em um conjunto de textos ("texts"), calcula os vetores
# ("embeddings") para ambos, e então classifica os textos com base na
# similaridade com a consulta. A similaridade é medida usando similaridade de
# cosseno e distância euclidiana.
#
# O script demonstra como usar vetores para realizar pesquisa semântica,
# permitindo encontrar textos relevantes com base no significado em vez de
# correspondência de palavras indexadas.
#
# ==============================================================================

# %%
# Imports.

import numpy as np
from nomic import embed
from lib.vectors import euclidean_distance, cosine_similarity

# %%
# Inputs.

# Define a expressão a ser utilizada na pesquisa.
query = "What is the best programming language?"

# Define os textos a serem consultados na pesquisa.
texts = [
  "Most used programming languages among developers worldwide as of 2024",
  "Why is processing a sorted array faster than processing an unsorted array?",
  "How do I undo the most recent local commits in Git?",
  "How do I delete a Git branch locally and remotely?",
  "What is the difference between 'git pull' and 'git fetch'?",
  "What does the \"yield\" keyword do in Python?"
  "How can I remove a specific item from an array in JavaScript?",
  "How can I rename a local Git branch?",
  "Which JSON content type do I use?",
  "How do I undo 'git add' before commit?",
  "What is the '-->' operator in C/C++?",
  "How do I force \"git pull\" to overwrite local files?",
  "Can comments be used in JSON?",
  "What and where are the stack and heap?",
  "Why does HTML think “chucknorris” is a color?",
  "How do I check out a remote Git branch?",
  "How can I remove a specific item from an array in JavaScript?",
  "How do I check if an element is hidden in jQuery?",
  "What does \"use strict\" do in JavaScript, and what is the reasoning behind it?",
  "How do I redirect to another webpage?",
  "var functionName = function() {} vs function functionName() {}",
  "What does the \"yield\" keyword do in Python?",
  "What does if __name__ == \"__main__\": do?",
  "Does Python have a ternary conditional operator?",
  "How can I validate an email address in JavaScript?",
  "How do I check whether a checkbox is checked in jQuery?",
  "How can I horizontally center an element?",
  "Should we MAC-then-encrypt or encrypt-then-MAC?",
  "What are the differences between a digital signature, a MAC and a hash?",
  "How much would it cost in U.S. dollars to brute-force a 256-bit key in a year?",
  "Time Capsule cryptography?",
  "Why is elliptic curve cryptography not widely used, compared to RSA?",
  "What are some of the best programming languages to learn?",
  "Do you wear cosmetics to work that you do not use on your leisure days?"
]

# %%
# Processamento dos vetores dos textos a serem consultados na pesquisa.

# Calcula os vetores dos textos.
embeddings = embed.text(
  dimensionality=128,
  texts=texts,
  model='nomic-embed-text-v1.5',
  inference_mode="local",
)

# Define a base de dados dos textos com seus respectivos vetores.
database = [{ 'text': x, 'vectors': y }  for x, y in zip(texts, embeddings['embeddings'])]

# %%
# Processamento da pesquisa.

# Calcula os vetores da expressão de pesquisa.
query_data = {
  'text': query,
  'vectors': embed.text(
    dimensionality=128,
    texts=[query],
    model='nomic-embed-text-v1.5',
    inference_mode='local'
  )['embeddings'][0]
}

result = sorted( # Ordena o resultado da pesquisa.
    [
      {
        'document': item,
        # Calcula a similaridade por coseno entre os vetores da expressão e os vetores do item atual.
        'cosine_similarity': cosine_similarity(np.array(query_data['vectors']), np.array(item['vectors'])),
        # Calcula a distância euclidiana entre os vetores da expressão e os vetores do item atual.
        'euclidean_distance': euclidean_distance(np.array(query_data['vectors']), np.array(item['vectors'])),
      } for item in database
    ],
    # Chave para ordenação.
    key=lambda x: x['cosine_similarity'],
    # Ordem decrescente.
    reverse=True
)

# %%
# Impressão do resultado.

print("Query:", query)
print()
print("Results:")

for doc in result:
  print("[cos(θ): " + ('%.4f' % doc['cosine_similarity']) + ", ∆: "+ ('%.4f' % doc['euclidean_distance']) + "]:", doc['document']['text'])

# %%
