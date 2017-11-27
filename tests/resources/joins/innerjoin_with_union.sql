insert into foo( a, b, c )
select
a.d, a.e, b.f
from 
    foo a inner join bar b on a.x = b.x
where
    b.t = '2'
union
select
c.d, c.e, d.f
from
    def c inner join xyz d on c.x = d.x
where 
    c.s = d.s
