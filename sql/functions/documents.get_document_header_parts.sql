DROP FUNCTION IF EXISTS documents.get_document_parents_parts;

CREATE OR REPLACE FUNCTION documents.get_document_parents_parts(p_id INTEGER)
RETURNS TABLE(
  "id"                INTEGER,
  "parent_id"         INTEGER,
  "type"              CHARACTER VARYING,
  "ref"               CHARACTER VARYING,
  "text"              CHARACTER VARYING
)
LANGUAGE SQL
AS $$
  -- Gets the document's part.
  SELECT
      part.id,
      part.parent_id,
      part.type,
      part.ref,
      part.text
      FROM documents.parts doc
      CROSS JOIN documents.get_document_parents_parts(doc.parent_id) part -- RECURSION
      WHERE doc.id = p_id

  UNION ALL
  -- Get the parent's part.
      SELECT
          parent.id,
          parent.parent_id,
          parent.type,
          parent.ref,
          parent.text

          FROM documents.parts doc

          INNER JOIN documents.parts parent
              ON doc.parent_id = parent.id

          WHERE doc.id = p_id

$$;
