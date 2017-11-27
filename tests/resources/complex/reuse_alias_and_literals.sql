INSERT INTO foo (my_literal, typeid)
SELECT 'LITERAL\',
  1 as typeid /* original level */
from
  (select distinct
    pgru.typeid
  from
    database.schema.app_abc pgru
    inner join database.schema.app_xyz pg on pg.xyzid = pgru.xyzid
    inner join database.schema.app_def pgp on pgp.xyzid = pg.xyzid
    inner join database.schema.app_tuv pp on pp.tuvid = pgp.tuvid and
                                             ((pgru.tuvtypeid is null) or
                                              (pgru.tuvtypeid = pp.tuvtypeid))) qwetuvtype
  inner join database.schema.app_qwe u on u.qweid = qwetuvtype.qweid

union all
select
  'LITERAL\',
  2 as typeid /* second level */
from
  (select distinct
    pgru.qweid,
    pgru.xyzroleid,
    pp.brandid,
    pg.fghid
  from
    database.schema.app_abc pgru
    inner join database.schema.app_xyz pg on pg.xyzid = pgru.xyzid
    inner join database.schema.app_def pgp on pgp.xyzid = pg.xyzid
    inner join database.schema.app_tuv pp on pp.tuvid = pgp.tuvid and
                                             ((pgru.tuvtypeid is null) or
                                              (pgru.tuvtypeid = pp.tuvtypeid))
  where
    pgru.xyzroleid in (2) /* fsd;fkl sfsd; lfksdfsd f */ ) brands
  inner join database.schema.app_tuv pb on pb.brandid = brands.brandid
  inner join database.schema.app_qwe u on u.qweid = brands.qweid
union all
select
  'LITERAL\',
  3 as typeid /* third level */
from
  (select distinct
    pgru.qweid,
    pgru.xyzroleid,
    pp.brandid,
    pg.fghid
  from
    database.schema.app_abc pgru
    inner join database.schema.app_xyz pg on pg.xyzid = pgru.xyzid
    inner join database.schema.app_def pgp on pgp.xyzid = pg.xyzid
    inner join database.schema.app_tuv pp on pp.tuvid = pgp.tuvid and
                                             ((pgru.tuvtypeid is null) or
                                              (pgru.tuvtypeid = pp.tuvtypeid))
  where
    pgru.xyzroleid in (4) /* hxgfhfhf fhfg dh ghf  */ ) brands
  inner join database.schema.app_tuv pb on pb.brandid = brands.brandid
  inner join database.schema.app_qwe u on u.qweid = brands.qweid

union all
select
  'LITERAL\', 4 AS typeid /* fourth level */
FROM
  (SELECT DISTINCT pgru.qweid,
                   pgru.xyzroleid,
                   CASE
                       WHEN fgh2.fghid2 IS NULL THEN pg.fghid
                       ELSE fgh2.fghid2
                   END AS fghid
   FROM database.schema.app_abc pgru
   INNER JOIN database.schema.app_xyz pg ON pg.xyzid = pgru.xyzid
   LEFT JOIN
     (SELECT t.fghid,
             tt.fghid AS fghid2
      FROM database.schema.app_fgh t
      CROSS JOIN
        (SELECT *
         FROM database.schema.app_fgha t
         WHERE t.fghid IN (1,
                           2044,
                           2045)) tt
      WHERE t.fghid IN (1,
                        2044,
                        2045)
        AND t.fghid <> tt.fghid) fgh2 ON fgh2.fghid = pg.fghid /* some funny comment */ ) fghs
INNER JOIN database.schema.app_xyz pg ON pg.fghid = fghs.fghid
INNER JOIN database.schema.app_def pgp ON pgp.xyzid = pg.xyzid
INNER JOIN database.schema.app_tuv pp ON pp.tuvid = pgp.tuvid
INNER JOIN database.schema.app_qwe u ON u.qweid = fghs.qweid