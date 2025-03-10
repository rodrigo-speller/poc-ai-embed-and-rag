DELETE FROM vectors.questions q
  USING vectors.documents d
  WHERE d.doc_part_id = q.doc_part_id
    AND q.e5_query_768 IS NOT NULL
    AND (d.e5_passage_768 <=> q.e5_query_768 > 0.1)
