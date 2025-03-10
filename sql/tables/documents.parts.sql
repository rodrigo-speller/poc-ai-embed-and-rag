CREATE TABLE IF NOT EXISTS "documents"."parts" (
  "id"              INTEGER NOT NULL,
  "parent_id"       INTEGER,
  "type"            CHARACTER VARYING NOT NULL,
  "ref"             CHARACTER VARYING,
  "text"            CHARACTER VARYING NOT NULL,
  CONSTRAINT "parts_pkey"
    PRIMARY KEY ("id"),
  CONSTRAINT "parts_parent_id_fk"
    FOREIGN KEY ("parent_id")
    REFERENCES "documents"."parts" ("id")
)
;

CREATE INDEX IF NOT EXISTS "fki_parts_parent_id"
  ON "documents"."parts" ("parent_id")
;

CREATE INDEX IF NOT EXISTS "idx_parts_type"
  ON "documents"."parts"
  ("type" varchar_ops)
;
