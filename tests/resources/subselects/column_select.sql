insert into foo( a, b, c )
select 
  convert(datetime, datediff(day, 0, a.b)) abdatetime,
  convert(numeric(15,4), case
                         when exists (select
                                            'x'
                                          from
                                            db.schema.bar c
                                          where
                                            c.some_id is not null and
                                            c.some_id = a.some_id)
                         then 2
                       else 1 end) as otherid,
  a.c
from
  db.schema.table a
  inner join db.schema.table d on a.some_id = d.some_id
where
  a.some_column = 'y'
