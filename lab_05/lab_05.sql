
-- 1.
SELECT row_to_json(P) result FROM PLAYER P;
SELECT row_to_json(C) result FROM "character" C;
SELECT row_to_json(A) result FROM ADVENTURE A;

-- 2. Выполнить загрузку и сохранение JSON файла в таблицу.

CREATE TABLE if not exists character_copy (
    id int PRIMARY KEY,
    player_id int,
    "name" text, 
    "level" int CHECK("level" between 1 and 21),
    race text,
    gender text CHECK(gender in ('Муж.', 'Жен.')),
    background text,
    alignment text,
    is_alive boolean,

    FOREIGN KEY (player_id) references player(id)
);

COPY
(
    SELECT row_to_json(c) result FROM "character" c
)
TO '/mnt/character.json';

COPY character
TO '/mnt/character.csv'
DELIMITER ';';

CREATE TABLE IF NOT EXISTS character_import(doc json);

COPY character_import FROM '/mnt/character.json';
    
INSERT INTO character_copy
SELECT id, player_id, "name", "level", race, gender, background, alignment, is_alive
FROM character_import, json_populate_record(null::character_copy, doc);

SELECT * F	ROM character_copy;

CREATE TABLE IF NOT EXISTS character_json
(
    data json
);


-- 3. Создать таблицу, в которой будет атрибут(-ы) с типом JSON, или

CREATE TABLE IF NOT EXISTS blacklist_json
(
    data json
);

SELECT * FROM blacklist_json;

INSERT INTO blacklist_json
SELECT * FROM json_object('{player_id, reason}', '{1, "Красноречиво выражался"}');

-- 4. Выполнить следующие действия:
-- 1. Извлечь XML/JSON фрагмент из XML/JSON документа
CREATE TABLE IF NOT EXISTS character_name_tmp
(
    id int,
    "name" text
);

SELECT id, "name"
FROM character_import, json_populate_record(null::character_name_tmp, doc)
WHERE "name" LIKE 'А%';

SELECT * FROM character_import;

-- 2. Извлечь значения конкретных узлов или атрибутов XML/JSON документа

SELECT doc->'id' as id, doc->'name' as "name"
FROM character_import;


-- 3. Выполнить проверку существования узла или атрибута

CREATE TABLE inventory(doc jsonb);
-- Оружие: огнестрельное: пистолет, ручное: нож
INSERT INTO inventory VALUES ('{"id":0, "weapon": {"hand":"sword", "shield":"true"}}');
INSERT INTO inventory VALUES ('{"id":1, "weapon": {"hand":"waraxe gun", "shield":"false"}}');

CREATE OR REPLACE FUNCTION get_inventory(i jsonb)
RETURNS VARCHAR AS '
    SELECT CASE
               WHEN count.cnt > 0
                   THEN ''true''
               ELSE ''false''
               END AS comment
    FROM (
             SELECT COUNT(doc -> ''id'') cnt
             FROM inventory
             WHERE doc -> ''id'' @> i
         ) AS count;
' LANGUAGE sql;

SELECT * FROM inventory;

SELECT get_inventory('1');

-- 4. Изменить XML/JSON документ

INSERT INTO inventory VALUES ('{"id":3, "weapon": {"hand":"pike", "shield":"false"}}');

SELECT * FROM inventory;
SELECT doc || '{"id": 33}'::jsonb
FROM inventory;

UPDATE inventory
SET doc = doc || '{"id": 33}'::jsonb
WHERE (doc->'id')::INT = 3;

SELECT * FROM inventory;

-- 5. Разделить XML/JSON документ на несколько строк по узлам

CREATE TABLE IF NOT EXISTS passed_game(doc JSON);

INSERT INTO passed_game VALUES ('[{"user_id": 0, "game_id": 1},
  {"user_id": 2, "game_id": 2}, {"user_id": 3, "game_id": 1}]');

SELECT * FROM passed_game;

-- jsonb_array_elements - Разворачивает массив JSON в набор значений JSON.
SELECT jsonb_array_elements(doc::jsonb)
FROM passed_game;


