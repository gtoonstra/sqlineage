insert into foo( a, b, c )
select
a.d, a.e, b.f
from 
    foo a inner join bar b
where
    1 = 1
