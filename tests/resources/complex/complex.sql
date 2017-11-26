DECLARE @cutoffdate date
SET @CUTOFFDATE = '19990101';--here goes some kind of comment

DECLARE @SPECIALCODE int
SET @SPECIALCODE = 6767;

--another comment here
WITH somedata -- explanation of what this does
 -- and some sloppy continuation of the comment
AS
  (SELECT foo.a ,
          foo.b ,
          foo.c ,
          foo.d ,
          foo.e ,
          foo.f ,
          foo.g ,
          foo.h ,
          foo.k ,
          ISNULL(foo.m, 9999) AS m ,
          foo.p ,
          foo.q ,
          foo.s ,
          SUM(foo.w) OVER (PARTITION BY foo.b,
                                        foo.a) AS w ,
                          rank
   FROM
     ( SELECT bar.a ,
              bar.b ,
              bar.c ,
              bar.d ,
              bar.e ,
              bar.f ,
              bar.g ,
              bar.h ,
              bar.k ,
              ISNULL(bar.m, 9999) AS m ,
              bar.p ,
              bar.q ,
              ref.s , -- another comment to explain something
 COUNT(COALESCE(bar.m, 1)) AS w ,
 RANK() OVER (PARTITION BY bar.b
              ORDER BY bar.a DESC) AS rank ,
             ROW_NUMBER() OVER (PARTITION BY bar.b,
                                             bar.m,
                                             bar.a
                                ORDER BY bar.c DESC) AS ROW
      FROM database.schema.table bar
      LEFT JOIN database.schema.other_table REF ON ref.b = bar.b
      GROUP BY bar.a ,
               bar.b ,
               bar.c ,
               bar.d ,
               bar.e ,
               bar.f ,
               bar.g ,
               bar.h ,
               bar.k ,
               ISNULL(bar.m, 9999) ,
               bar.p ,
               bar.q ,
               ref.s ,
               bar.m ) foo
   WHERE ROW = 1 )
INSERT INTO destination_table
SELECT def.date ,
       def.b ,
       def.c ,
       def.d ,
       def.e ,
       def.f ,
       def.g ,
       def.h ,
       def.k ,
       def.p ,
       def.q ,
       def.m ,
       def.counter ,
       def.Minutes ,
       def.Hours ,
       def.Days
FROM
  (-- another explanatory comment
 SELECT CONVERT(DATE, (CONVERT(VARCHAR, C.date))) AS Date ,
        sd.b ,
        sd.c ,
        sd.d ,
        sd.e ,
        sd.f ,
        sd.g ,
        sd.h ,
        sd.k ,
        sd.p ,
        sd.q ,
        sd.m ,
        C.counter AS counter -- comment line 1
 -- comment line 2
 -- comment line 3
 ,
        cast((CASE
                  WHEN C.counter = @SPECIALCODE THEN COALESCE(Pm.prest, Pm.weekpres2)
                  ELSE C.counter_value
              END) AS numeric(14,5)) / sd.w AS Minutes ,
        cast(CASE
                 WHEN C.counter = @SPECIALCODE THEN COALESCE(Pm.prest, Pm.rprest, Pm.weekpres2)
                 ELSE C.counter_value
             END AS numeric(14,5)) / 60 / sd.w AS Hours ,
        cast(CASE
                 WHEN C.counter = @SPECIALCODE THEN COALESCE(Pm.prest, Pm.rprest, Pm.weekpres2)
                 ELSE C.counter_value
             END AS numeric(14,5)) / 480 / sd.w AS Days
   FROM database.schema.table1 AS C
   LEFT JOIN database.schema.pcur_table Cu ON Cu.specialnr = C.specialnr
   INNER JOIN database.schema.pcount_table Co ON Co.counter = C.counter
   INNER JOIN database.schema.pac pac ON Pac.countercode LIKE Co.code -- another explanatory comment

   INNER JOIN somedata sd ON sd.s = Cu.employeenr COLLATE latin1_general_ci_as -- explains what this does

   AND DATEADD(m, DATEDIFF(m, 0, CONVERT(DATE, (CONVERT(VARCHAR, C.bookdate)))), 0) = sd.a
   INNER JOIN database.schema.pcam pm ON pm.bookdate = C.bookdate -- table that is referenced elsewhere

   AND C.specialnr = Pm.specialnr
   WHERE -- another explanatory comment
 somenr <> ''
     AND name NOT LIKE '%Test%'
     AND DATEADD(m, DATEDIFF(m, 0, CONVERT(DATE, (CONVERT(VARCHAR, C.bookdate)))), 0 ) IN
       ( SELECT sd.a
        FROM somedata sd )
   UNION ALL -- simulates a standard row in a dimension table for example
 SELECT CONVERT(DATE, (CONVERT(VARCHAR, f.bookdate))) AS Date ,
        f.b ,
        f.c ,
        f.d ,
        f.e ,
        f.f ,
        f.g ,
        f.h ,
        f.k ,
        f.p ,
        f.q ,
        f.m ,
        f.counter AS counter ,
        f.Minutes ,
        f.Hours ,
        f.Days
   FROM flat_table f ) def
WHERE def.date >= @CUTOFFDATE
