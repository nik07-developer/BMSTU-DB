
-- Скалярная ф
-- Количество смертей персонажа
create or replace function my_count(cid integer) returns int as $$
	SELECT count(*)
	from death d
	where d.CHARACTER_ID = cid
$$ LANGUAGE sql;

select * from DEATH D 

select id, "name", my_count(id) as dead_count
from "character" c ;

-- Табличная Ф
-- Таблица смертей персонажа
create or replace function my_table(cid integer) 
returns table (reason text, last_words text) as $$
	select DEATH_REASON, LAST_WORDS
	from death d
	where d.CHARACTER_ID = cid
$$ LANGUAGE sql;

select * from my_table(1130);


-- Многооператорная Табличная Ф
-- Таблица смертей игрока
create or replace function my_table2(cid integer)
returns table (reason text, last_words text) as $$
declare
	newcid int;
begin
	newcid := cid + 1;

	return query (select death.DEATH_REASON, death.LAST_WORDS
				  from death
				  where death.CHARACTER_ID = newcid);
end $$ language plpgsql;

select * from my_table2(1129);


-- Рекурсивная Ф
create or replace function factorial(n int)
returns int as $$
begin
	if n > 1 then return n * factorial(n - 1); end if;
	return 1;
END $$ language plpgsql;

select factorial(5);

-- Хранимая процедура
-- Вывести кол-во смертей персонажа в отдельную таблицу
create or replace procedure proc_count(cid integer) as $$
	drop table if exists DEADS_T;

	select cid as "Id", count(*) as "Deads Count"
	into temp deads_t
	from death d
	where d.CHARACTER_ID = cid;
$$ LANGUAGE sql;

call proc_count(1130);
select * from deads_t;

create or replace procedure character_dies(cid integer) as $$
	drop table if exists DEADS_T;

	select cid as "Character ID", d.ID as "Death Id", death_reason as "Reason"
	into temp dies_t
	from death d
	where d.CHARACTER_ID = cid;
$$ LANGUAGE sql;

call character_dies(1130);
select * from dies_t;


-- Рекурсивная Процедура
create or replace procedure rec_proc(n int) as $$
begin
	create table if not exists ttt(
		id int primary key,
		value int
	);
	
	insert into ttt values (n, n * n);
	if n > 1 then call REC_PROC(n - 1); end if;
end $$
language plpgsql;

drop table ttt;

call rec_proc(20);

select * from ttt;


-- Процедура с курсором
create or replace procedure proc_update(find int, newval int) as $$
declare
	cur record;
	curs cursor for (
		select id, value from ttt
	);
begin
	open curs;
	loop
		fetch curs into cur;
		exit when not found;
	
		update ttt
			set value = newval
			where id = cur.id and cur.value = find;
	end loop;
end $$ language plpgsql;

call proc_update(400, 399);

select * from ttt


-- Хранимая процедура доступа к метаданным
create or replace procedure meta_count(filtr text, out res int) as $$
begin
	res := (select count(table_name) from information_schema.tables
			where table_name like filtr);
end $$
language plpgsql;


-- DML After Update
create or replace function funny_trigger()
returns trigger as $$
begin
	if new.id <> old.id then 
		update ttt
		set value = id * id
		where id = new.id;
	end if;
	return new;
end $$
language plpgsql;

create or replace trigger sus after update
on ttt
for each row
execute function funny_trigger();

select * from ttt;

update ttt
set id = id + 1
where id = 20;

-- DML Instead Of
create or replace function funny_instead_trigger()
returns trigger as $$
begin 
	update ttt
	set id = -id
	where id = old.id;
	return new;
end $$
language plpgsql;

create view ttt_view as
	select id, value
	from ttt;

create or replace trigger ssuss instead of delete
on ttt_view
for each row 
execute function funny_instead_trigger();

select * from ttt;

delete from ttt_view
where id = 21;


--
drop function find_adventure;

select * from ADVENTURE A;

select * from PARTY P where P.CHARACTER_ID = 6;

create or replace function find_adventure(cid integer, g text) 
returns table (character_id int, adventure_id int, genre text) as $$
	select cid, a.id, a.genre
	from adventure a
	where lower(a.GENRE) like g
	and EXISTS (select * 
				from party p1 
				where p1.ADVENTURE_ID  = a.ID and p1.CHARACTER_ID = cid)				
$$ LANGUAGE sql;

select * from FIND_ADVENTURE(6, 'хоррор');




