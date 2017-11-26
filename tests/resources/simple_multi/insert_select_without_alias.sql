insert into foo( a, b, c )
SELECT
    CASE
       WHEN abc.factor > 0
          THEN abc.factor
       ELSE def.factor
    END AS factor,
    def.scale
  FROM
    (SELECT
         s.b
       FROM
         database.schema.app_xyz s) s
    INNER JOIN database.schema.app_xyz abc ON abc.xyzcategoryid = s.b
    LEFT JOIN database.schema.app_zxc def ON def.c = abc.c;