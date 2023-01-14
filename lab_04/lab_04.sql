create extension plpython3u;

select * from pg_language;

-- 1 Скалярная функция
-- Получить имя персонажа
CREATE OR REPLACE FUNCTION get_character_name(id int)
RETURNS VARCHAR AS $$
res = plpy.execute(f"\
    SELECT name \
    FROM character c \
    WHERE c.id = {id};")
if res:
    return res[0]['name']
$$ LANGUAGE plpython3u;

SELECT * FROM get_character_name(1129) as "World name";


-- 2) Агрегатная функция CLR.
-- Получить кол-во педставителей расы
CREATE OR REPLACE FUNCTION count_race(race text)
RETURNS INT AS $$
count = 0
res = plpy.execute("SELECT * FROM character")

for elem in res:
    if elem["race"].lower() == race.lower():
        count += 1

return count
$$ LANGUAGE plpython3u;

SELECT * FROM count_race('человек');

-- 3) Табличная функция CLR.
-- Получить новый список классов

drop function find_deathes;

select * from DEATH D;

CREATE OR REPLACE FUNCTION find_deathes(cid int)
RETURNS table (character_id int, death_reason text, last_words text) AS $$
rv = plpy.execute(f" \
	SELECT character_id, death_reason, last_words\
	FROM death")
res = []
for elem in rv:
    if elem["character_id"] == cid:
        res.append(elem)
return res
$$ LANGUAGE plpython3u;

select * from FIND_DEATHES(1130);


--4 Процедура CLR
select * from PLAYER P;

CREATE OR REPLACE PROCEDURE add_player
(
    p_name text,
    p_gender text,
    p_city text,
    p_birthday date
    
) AS $$
	plpy.execute(f"INSERT INTO player(name, gender, city, birthday) VALUES('{p_name}','{p_gender}', '{p_city}', '{p_birthday}');")
$$ LANGUAGE plpython3u;

CALL add_player('Никита', 'Муж.', 'Воронеж', date('2022-01-01'));


-- 5) Триггер CLR.
-- Создаем представление, т.к. таблицы не могут иметь INSTEAD OF triggers.
CREATE VIEW players_new AS
SELECT *
FROM player
WHERE id < 16;

SELECT * FROM players_new;

UPDATE PLAYERS_NEW 
set name = 'Никита'
where id = 2;

CREATE OR REPLACE FUNCTION del_player_func()
RETURNS trigger AS $$
old_id = TD["old"]["id"]
rv = plpy.execute(f"UPDATE players_new \
					SET name = \'none\', city = \'none\'  \
					WHERE players_new.id = {old_id}")
return TD["new"]
$$ LANGUAGE plpython3u;

CREATE or replace TRIGGER del_player_trigger
INSTEAD OF DELETE ON players_new
FOR EACH ROW
EXECUTE PROCEDURE del_player_func();

DELETE FROM players_new
WHERE "name" = 'Никита';


-- 6) Определяемый пользователем тип данных CLR.
CREATE TYPE dungeon_master AS
(
	id int,
	adventure_count int
);

select * from ADVENTURE A;

SELECT master_id as id, COUNT(*) as cnt  
				   FROM adventure         
			       WHERE master_id = 43  
				   GROUP BY master_id;

CREATE OR REPLACE FUNCTION get_dm(mid int)
RETURNS dungeon_master as $$
rv = plpy.execute(f"SELECT master_id as id, COUNT(*) as cnt  \
				   FROM adventure a       \
			       WHERE a.master_id = '{mid}'  \
				   GROUP BY master_id;")
if (rv.nrows()):
    return (rv[0]["id"], rv[0]["cnt"])
$$ LANGUAGE plpython3u;

SELECT get_dm(43);

--- Защита:

CREATE OR REPLACE FUNCTION teremok(id int)
RETURNS text AS $$
rv = plpy.execute(f"\
    SELECT name, gender \
    FROM character c \
    WHERE c.id = {id};")
if rv:
	tmp = 'Зравствуйте, '
	if rv[0]['gender'] == 'Муж.':
		tmp = tmp + 'сударь '
	else:
		tmp = tmp + 'сударыня '
	tmp = tmp + rv[0]['name']
	return tmp
$$ LANGUAGE plpython3u;

SELECT teremok(41)



