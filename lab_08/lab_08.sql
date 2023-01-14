CREATE TABLE if not exists death (
    id SERIAL PRIMARY KEY,
    character_id int,
    death_reason text, 
    last_words text,
    "date" date,

    FOREIGN KEY (character_id) references "character"(id)
);

select * from death limit(10);