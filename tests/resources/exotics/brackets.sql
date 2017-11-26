insert into foo( a, b, c, d )
select 
      a,
      b,
      c,
      d
from 
      [server].[database].[schema].[table]
