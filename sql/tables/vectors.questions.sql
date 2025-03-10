CREATE TABLE IF NOT EXISTS "vectors"."questions" (
  "id"                SERIAL NOT NULL,
  "doc_part_id"       INTEGER NOT NULL,
  "question"          CHARACTER VARYING NOT NULL,
  "e5_query_768"      VECTOR(768),
  CONSTRAINT "questions_pkey"
    PRIMARY KEY ("id"),
  CONSTRAINT "questions_doc_part_id_fk"
    FOREIGN KEY ("doc_part_id")
    REFERENCES "documents"."parts" ("id")
)
;

CREATE INDEX IF NOT EXISTS "fki_questions_doc_part_id"
  ON "vectors"."questions" ("doc_part_id")
;