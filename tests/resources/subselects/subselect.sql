INSERT INTO subselects( a )

SELECT
    foo.a
  FROM (
       SELECT DISTINCT
           b.a
         FROM foo.bar.tablename b
         WHERE b.a IS NOT NULL
       UNION
       SELECT DISTINCT
           c.a
         FROM abc.dbo.xyz c

       UNION
       SELECT DISTINCT
           d.a
         FROM abc.def.xyz d
         WHERE DATEPART (weekday, GETDATE ()) = 1) foo;
