INSERT INTO subselects( a )

/** some commments */

SELECT
    foo.a
  FROM (
       SELECT DISTINCT
       /* another comment */
           b.a
         FROM foo.bar.tablename b
         WHERE b.a IS NOT NULL
       UNION
       SELECT DISTINCT
       /* new a's too */
           c.a
         FROM abc.dbo.xyz c

       UNION
       SELECT DISTINCT
           d.a
         FROM abc.def.xyz d
         WHERE DATEPART (weekday, GETDATE ()) = 1) foo;
