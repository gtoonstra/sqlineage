INSERT INTO subselects( a )

SELECT
    foo.a
  FROM (
       SELECT DISTINCT
           b.a
         FROM foo.bar.tablename b
      ) foo;
