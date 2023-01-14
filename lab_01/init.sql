CREATE TABLE if not exists player (
    id SERIAL PRIMARY KEY,
    "name" text, 
    gender text CHECK(gender in ('Муж.', 'Жен.')),
    city text,
    birthday date
);

CREATE TABLE if not exists "character" (
    id SERIAL PRIMARY KEY,
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

CREATE TABLE if not exists death (
    id SERIAL PRIMARY KEY,
    character_id int,
    death_reason text, 
    last_words text,
    "date" date,

    FOREIGN KEY (character_id) references "character"(id)
);

CREATE TABLE if not exists adventure (
    id SERIAL PRIMARY KEY,
    master_id int,
    "name" text,
    game_world text, 
    genre text,
    deus_ex_machina_count int CHECK(deus_ex_machina_count >= 0),
    robbed_caravans_count int CHECK(robbed_caravans_count >= 0),

    FOREIGN KEY (master_id) references player(id)
);

CREATE TABLE if not exists "class" (
    id int PRIMARY KEY,
    "name" text,
    "description" text
);

CREATE TABLE if not exists progress (
    character_id int,
    class_id int,
    "level" int CHECK("level" between 1 and 20),

    PRIMARY KEY (character_id, class_id),
    FOREIGN KEY (character_id) references "character"(id),
    FOREIGN KEY (class_id) references class(id)
);

CREATE TABLE if not exists party (
    adventure_id int,
    character_id int,
    
    PRIMARY KEY (adventure_id, character_id),
    FOREIGN KEY (adventure_id) references "adventure"(id),
    FOREIGN KEY (character_id) references "character"(id)
);

SELECT * FROM "character" c 


	


