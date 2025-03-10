import psycopg2

def connect():
  return psycopg2.connect(
    database = "postgres",
    user = "postgres",
    host= '127.0.0.1',
    password = "local",
    port = 5432
  )