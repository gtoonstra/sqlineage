insert into foo( a, b, c, d )
select 
      a,
      b,
      c,
      d
from 
      `database.schema with a space.table with something else`
