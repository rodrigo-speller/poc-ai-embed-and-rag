import numpy as np

def euclidean_distance(a, b):
  return np.linalg.norm(a - b, 2)

def cosine_similarity(a, b):
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def ang_similarity(a, b):
  return 1 - np.acos(cosine_similarity(a, b)) / np.pi
