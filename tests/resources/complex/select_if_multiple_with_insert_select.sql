DECLARE @z DATETIME; 
SELECT  @z = COALESCE(MAX(a), '2000-01-01')
FROM    db.s.foo;

IF ( DATEDIFF(MONTH, @z, GETDATE()) > 1 )
    BEGIN

        WITH    afoo
                  AS ( SELECT   a, b, c
                       FROM     db.schema.bar bar
                       GROUP BY a, b, c
                     ) ,
                bfoo
                  AS ( SELECT   a, b, c
                       FROM     db.schema.bas bas
                       GROUP BY a, b, c
                     )
            INSERT  INTO db2.foo.zxc
                    ( a, b, c )
                    SELECT  a, b, c
                    FROM    db.schema.foo foo
                            INNER JOIN afoo ON afoo.e = foo.e
                            INNER JOIN bfoo ON bfoo.f = foo.f
                    WHERE               
                            foo.v = GETDATE()
                            AND foo.w IS NOT NULL;
   
    END; 
