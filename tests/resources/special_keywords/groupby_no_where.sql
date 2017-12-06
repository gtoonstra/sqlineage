INsert into foo(a, b, c)
select
        a,
        b,
        c
from
        db.schema.foo
group by
        a, b, c
