# This is installing the pgvector extension for postgres
FROM postgres:17.2 AS pgvectg

RUN apt-get update \
    && apt-get install -y \
      postgresql-17-pgvector \
    && rm -rf /var/lib/apt/lists/*
