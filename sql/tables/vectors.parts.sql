CREATE TABLE IF NOT EXISTS "vectors"."parts" (
  "doc_part_id"         INTEGER NOT NULL,
  "e5_passage_768"      VECTOR(768),
  "e5_query_768"        VECTOR(768),
  CONSTRAINT "parts_pkey"
    PRIMARY KEY ("doc_part_id"),
  CONSTRAINT "parts_doc_part_id_fk"
    FOREIGN KEY ("doc_part_id")
    REFERENCES "documents"."parts" ("id")
)
;
