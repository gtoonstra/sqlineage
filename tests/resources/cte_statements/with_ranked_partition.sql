WITH ranked AS (
   SELECT 
        a
      , b
      , c
      , d
      , e
      , f
      , RANK() OVER (
         PARTITION BY  
             a
           , b
         ORDER BY g desc
        ) as ranking
   FROM foo
)
select
    a
   ,b
   ,c
   ,d
   ,e
from ranked 
where ranking = 1
