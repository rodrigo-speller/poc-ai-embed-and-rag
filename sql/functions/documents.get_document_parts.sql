DROP FUNCTION IF EXISTS documents.get_document_parts;

CREATE OR REPLACE FUNCTION documents.get_document_parts(p_id INTEGER)
RETURNS TABLE(
  "id"                  INTEGER,
  "level"               INTEGER,
  "indent_level"        INTEGER,
  "parent_id"           INTEGER,
  "type"                CHARACTER VARYING,
  "ref"                 CHARACTER VARYING,
  "text"                CHARACTER VARYING
)
LANGUAGE SQL
AS $$
  -- Gets the document's part.
  SELECT
    doc.id,
    1,
    0,
    doc.parent_id,
    doc.type,
    doc.ref,
    doc.text
    FROM documents.parts doc
    WHERE doc.id = p_id

  UNION ALL
    -- Get child parts.
    SELECT * FROM (
      SELECT
        child.id,
        child.level + 1,
        child.indent_level + CASE WHEN doc.type IN ('paragrafo', 'inciso', 'alinea') THEN 1 ELSE 0 END,
        child.parent_id,
        child.type,
        child.ref,
        child.text
        FROM documents.parts doc
        CROSS JOIN documents.get_document_parts(doc.id) child -- RECURSION
        WHERE doc.parent_id = p_id
        ORDER BY child.id
    )
$$;
