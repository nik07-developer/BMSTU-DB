				  
create or replace function top_rogue(cnt integer)
returns table (ID int, "name" text, race text, character_level int, rogue_level int, adventure_id int, robbed_caravans int) as $$
with rogue as( 
	select ID, "name", race, t0."level" as character_level, P."level" as rogue_level, adventure_id, robbed_caravans
	from PROGRESS P 
	join (select *
		  from "character_copy" c 
		  join (select *
		  	    from PARTY P 
		 	    join (select A.ID as "aid", A.ROBBED_CARAVANS_COUNT as "robbed_caravans"
		  		      from ADVENTURE A) t2
		        on t2.aid = P.adventure_id) t1
	      on c.ID = t1.character_id) t0
	on P.CHARACTER_ID = t0.id
	where exists (select * 
				  from "class" cl 
				  where P.CLASS_ID = cl.ID and lower(cl."name") like '%плут%')
)
select *
from rogue R
order by robbed_caravans desc
limit cnt
$$ language sql;

select * from top_rogue(5);