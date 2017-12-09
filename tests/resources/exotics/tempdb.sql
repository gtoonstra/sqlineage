if object_id('tempdb..#temp', 'U') is not null
  drop table #temp

select
    distinct a.a
   ,b.b as cid1
   ,c.c as cid2
into #temp
from db.schema.a a
   inner join db.schema.b b on i.invoiceid = p.invoiceid
   inner join db.schema.c c on il.invoiceid = i.invoiceid
where
   not a.aid is null and
   b.zxc is null and
   c.cxz is null

select
   distinct a
from #temp
where cid1 = cid2

drop table #temp
