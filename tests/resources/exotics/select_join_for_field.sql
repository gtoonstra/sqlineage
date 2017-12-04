INSERT INTO foo( a, b, c)
SELECT  a.fooid
      , COALESCE(
          b.barid,
                 ( SELECT   c.d
                   FROM     db.schema.table e
                   WHERE    e.barid = a.barid
                 ),
                 ( SELECT   d.d
                   FROM     db.schema.xzc d
                            INNER JOIN db.schema.qwe q ON q.sid = d.sid
                   WHERE    q.qid = 0
                 ),
                  c.barid,
                 0) barid
      , f.iopid
FROM    db.schema.asd a
        INNER JOIN db.schema.pow pow ON pow.qid = a.qid
        INNER JOIN db.schema.jkl j ON pow.booid = j.booid
