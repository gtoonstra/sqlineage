insert into foo( a, b, c, d )
select
a.d, a.e, b.f, c.z
from 
    foo a left join bar b on a.x = b.x
    inner join (select f.p from ghi f where f.y = a.y) c on b.y = c.y
where
    b.t = '2'
union
select
c.d, c.e, d.f, e.z
from
    def c inner join xyz d on c.x = d.x
    left join (select f.p from ghi f where f.y = c.y) e on d.y = e.y
where 
    c.s = d.s
