-- comment
SELECT  a
      , CAST (CASE WHEN EXISTS ( SELECT 'x'
                                 FROM   db.schema.acac z
                                 WHERE  z.someid IS NOT NULL
                                 AND    z.someid = bar.someid )
                   THEN 2
                   ELSE 1
              END AS NUMERIC(38, 0)) AS b

      , COALESCE(
          aid, bid, 
                 ( SELECT   s.cid
                   FROM     db.schema.foo s
                   WHERE    s.sid = bar.sid
                 ),
                 ( SELECT   p.pid
                   FROM     db.schema.cxz p
                   WHERE    p.mid = 0
                 ), 0) c
      , d
FROM    db.schema.bar bar
UNION ALL
SELECT DISTINCT
        a
      , COALESCE(
          aid, bid, 
                 ( SELECT   s.cid
                   FROM     db.schema.foo s
                   WHERE    s.sid = bas.sid
                 ),
                 ( SELECT   p.pid
                   FROM     db.schema.cxz p
                   WHERE    p.mid = 0
                 ), 0) b
      , c
FROM    db.schema.bas bas
WHERE   bas.msg IS NULL;
