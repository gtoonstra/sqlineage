INSERT INTO foo(a, b, c)
SELECT
    a,
    b,
    c
  FROM (
       SELECT
           a,
           b,
           c
         FROM db.schema.view t WITH (nolock) 
       UNION ALL
       SELECT
           a,
           b,
           c
         FROM (SELECT
                   a,
                   b,
                   CASE
                      WHEN someid = 11111
                         THEN d
                      ELSE 0
                   END AS c,
                 FROM bar) def
         GROUP BY
           a,
           b) abc
  GROUP BY
    a,
    b
  ORDER BY
    a
    b;