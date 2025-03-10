CREATE TABLE IF NOT EXISTS "vectors"."documents" (
  "doc_part_id"       INTEGER NOT NULL,
  "e5_passage_768"    VECTOR(768),
  CONSTRAINT "documents_pkey"
    PRIMARY KEY ("doc_part_id"),
  CONSTRAINT "pdocuments_doc_part_id_fk"
    FOREIGN KEY ("doc_part_id")
    REFERENCES "documents"."parts" ("id")
)
;
