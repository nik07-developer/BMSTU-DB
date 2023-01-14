SELECT * from "character" c order by c."level";


---1
SELECT P."name", P.CITY 
	FROM PLAYER P
	WHERE P.CITY = 'Москва';

SELECT DISTINCT "name", GENDER, BIRTHDAY, CITY 
	FROM PLAYER P 
	WHERE BIRTHDAY  BETWEEN '2002-01-01' AND '2002-12-31';

SELECT DISTINCT "name", "level", race, gender, death_reason
	FROM "character" c JOIN DEATH d on c.ID = d.CHARACTER_ID 
	WHERE lower(d.DEATH_REASON) LIKE '%удар%' ;
	
SELECT MASTER_ID, "name", GAME_WORLD, GENRE, ROBBED_CARAVANS_COUNT 
	FROM ADVENTURE A
	WHERE MASTER_ID IN (SELECT id
 						FROM PLAYER P 
	 					WHERE city = 'Москва' )
		AND ROBBED_CARAVANS_COUNT > 5;
	
---5
SELECT "name", GENDER, BIRTHDAY, CITY 
from PLAYER P 
WHERE EXISTS ( SELECT ID
			   from ADVENTURE A
			   WHERE P.ID = A.MASTER_ID);
				
SELECT "name", race, gender, "level"
FROM "character" c 
WHERE "level" >= ALL ( SELECT "level"
 						FROM "character" h
 						where RACE = c.RACE);
 	
 						
select 	avg(Total) as "Actual AVG", 
		sum(Total) / count(id) as "Calc AVG"
from ( SELECT id, sum(deus_ex_machina_count) as Total
		FROM ADVENTURE a
 		GROUP BY id) AS ords;
	 

SELECT id, "name" as AdventureName, DEUS_EX_MACHINA_COUNT,
   (SELECT AVG(deus_ex_machina_count)
 	FROM adventure
 	WHERE adventure."name"  = a."name") AS AvgExCount,
   (SELECT MIN(deus_ex_machina_count)
	FROM adventure
 	WHERE adventure."name" = a."name" ) AS MinExCount
FROM ADVENTURE a;

			
SELECT "name", death_reason,
	case extract (year from "date")
 		WHEN extract (year from CURRENT_DATE) THEN 'This Year'
 		WHEN extract (year from CURRENT_DATE) - 1 THEN 'Last year'
 		ELSE text(extract (year from "date"))
 	END AS "Death Date"
FROM DEATH d join "character" c on d.CHARACTER_ID = c.ID ;


---10
SELECT id, master_id, GENRE, GAME_WORLD,
 	CASE
 		WHEN ROBBED_CARAVANS_COUNT < 5 THEN 'Unwanted'
 		WHEN ROBBED_CARAVANS_COUNT < 10 THEN 'Dangerous'
 		WHEN ROBBED_CARAVANS_COUNT < 15 THEN 'Very Dangerous'
 		ELSE 'Enemy of the Crown'
 	END AS "Robers Level"
FROM ADVENTURE A;
			

select id, "name", GENDER, RACE, "level" 
into temp honor_respect_beer
from "character" c
where IS_ALIVE and (LOWER(RACE) = 'гном' or LOWER(RACE) = 'дварф');

select * from honor_respect_beer;

drop table honor_respect_beer;


select level, is_alive, count(*)
from character
GROUP BY level, is_alive;


SELECT id, "name", GENDER, RACE, "level", DEATH_REASON
from "character" C 
join (select CHARACTER_ID, DEATH_REASON
	  from DEATH D 
	  where lower(D.DEATH_REASON) LIKE '%барсук%' ) dt
on C.ID = dt.CHARACTER_ID;


SELECT "name", GENDER, PERSON_NAME, PERSON_GENDER, PERSON_RACE, CITY, DEATH_REASON
from PLAYER P  
join (select id, "name" as PERSON_NAME, GENDER as PERSON_GENDER, RACE as PERSON_RACE, DEATH_REASON
	  from "character" C
	  join (select CHARACTER_ID, DEATH_REASON
	  		from DEATH D 
	  		where lower(D.DEATH_REASON) NOT LIKE '%старость%') cx
	  on C.ID = cx.CHARACTER_ID) cy
on P.ID = cy.ID;


SELECT CITY, min(P.BIRTHDAY), max(P.BIRTHDAY)
from PLAYER P
group by CITY;


---15
SELECT CITY, min(P.BIRTHDAY), max(P.BIRTHDAY)
from PLAYER P
group by CITY
HAVING COUNT(*) > 1;


INSERT into DEATH (CHARACTER_ID, DEATH_REASON, LAST_WORDS, "date")
values(null, 'Саблезубая белка', 'Ух ты какая лапочка', current_date);

select * from DEATH D where D."date" > date('2022-09-01');

INSERT into DEATH (CHARACTER_ID, DEATH_REASON, LAST_WORDS, "date")
select CHARACTER_ID, 'Опять барсук', 'На этот раз я готов', current_date
from DEATH D
where lower(DEATH_REASON) like '%барсук%';

select * from DEATH D WHERE lower(DEATH_REASON) like '%барсук%';

select * from DEATH D WHERE lower(DEATH_REASON) like '%опять%';

select * from "class" c;

UPDATE "class"
set DESCRIPTION = 'Луч света в тёмном царстве'
where "name" = 'Паладин' or "name" = 'Жрец';

update ADVENTURE A
set ROBBED_CARAVANS_COUNT = ROBBED_CARAVANS_COUNT + (select count(*)
													 from PARTY p
													 WHERE p.ADVENTURE_ID = A.ID)
where GENRE = 'Комедия';

SELECT GENRE, AVG(ROBBED_CARAVANS_COUNT)
from ADVENTURE A 
group by GENRE;

select race, count(*)
from character c
group by race;

---20
DELETE FROM DEATH D WHERE lower(DEATH_REASON) like '%опять%';

DELETE from PLAYER p
where ID not in (select PLAYER_ID 
				 from "character" c);


with cp(pid, max_lvl, char_count) as (
	select player_id, max("level"), count(*)
	from "character" c
	group by PLAYER_ID)
select avg(max_lvl) as "some text"
from cp;


with recursive abc(letter) as 
(
	select 'А'
	union all
	select chr(ASCII(letter) + 1)
	from abc
	where ASCII(letter) < ASCII('Я')
)
select letter, "name"
from "character" c left join abc on ASCII(c."name") = ASCII(abc.letter);


with tmp as(
	select P."name" as player_name, P.city, c."name" as character_name,
		min(c."level") over (partition by c."name") as min_level,
		max(c."level") over (partition by c."name") as max_level
	from "character" c left join "player" p on p.ID = c.PLAYER_ID
)
select * from tmp where min_level < max_level;	


---25
select "name", city
from (select "name", city,
		row_number() over(partition by "name", city) as cnt
	  from PLAYER P
) as tmp
where tmp.cnt = 1;


---Защита -- написать запрос, возвращающий топ персонажей-плутов по количеству ограбленных карованов

select * from "class" c;

select ROBBED_CARAVANS_COUNT from ADVENTURE A ;

with rogue as( 
	select ID, "name", race, t0."level" as character_level, P."level" as rogue_level, adventure_id, robbed_caravans
	from PROGRESS P 
	join (select *
		  from "character" c 
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
from rogue R1
where not EXISTS (select *
				  from rogue R2
				  where R1.robbed_caravans < R2.robbed_caravans);
			







			