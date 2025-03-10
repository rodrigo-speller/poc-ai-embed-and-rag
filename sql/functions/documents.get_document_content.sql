DROP FUNCTION IF EXISTS documents.get_document_content;

CREATE OR REPLACE FUNCTION documents.get_document_content(p_id INTEGER, p_include_header BOOLEAN = FALSE)
RETURNS CHARACTER VARYING
LANGUAGE SQL
AS $$
  SELECT
  STRING_AGG(
      REPEAT('  ', part.indent_level)
      || COALESCE(part.ref, '')
      ||  CASE WHEN LENGTH(COALESCE(part.ref, '')) = 0 THEN ''
        ELSE
          CASE part.type
          WHEN 'livro' THEN ': '
          WHEN 'cabecalho' THEN ': '
          WHEN 'inciso' THEN ' - '
          WHEN 'alinea' THEN ') '
          WHEN 'texto' THEN ': '
          ELSE ' '
          END
        END
      || part.text
    ,
    chr(10) ||
    chr(10)
  ) text

  FROM (
    SELECT 0 as indent_level, type, ref, text FROM documents.get_document_parents_parts(p_id)
      WHERE p_include_header
    UNION ALL
    SELECT indent_level, type, ref, text FROM documents.get_document_parts(p_id)
  ) part
$$;
