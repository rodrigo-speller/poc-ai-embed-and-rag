SELECT
  (v1.e5_query_768 <=> v2.e5_query_768),
  d1.id, d2.id,
  d1.text, d2.text

  FROM documents.parts d1

  INNER JOIN documents.parts d2
    ON d1.id < d2.id

  INNER JOIN vectors.parts v1
    ON d1.id = v1.doc_part_id

  INNER JOIN vectors.parts v2
    ON d2.id = v2.doc_part_id

  ORDER BY 1
