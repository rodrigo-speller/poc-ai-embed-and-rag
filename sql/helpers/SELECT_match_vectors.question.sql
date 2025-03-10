SELECT
  q.question,
  d.similarity "cos(θ)",
  d.doc_part_id,
  documents.get_document_content(d.doc_part_id),
  q.doc_part_id,
  documents.get_document_content(q.doc_part_id)
  
  FROM vectors.questions q

  CROSS JOIN LATERAL (
    SELECT q.e5_query_768 <=> d.e5_passage_768 similarity, *
      FROM vectors.documents d
      ORDER BY 1
      LIMIT 1
  ) d

  WHERE q.e5_query_768 IS NOT NULL AND d.doc_part_id != q.doc_part_id
  ORDER BY 1