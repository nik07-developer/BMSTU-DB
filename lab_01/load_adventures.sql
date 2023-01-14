
COPY "adventure" ("name", game_world, genre, master_id, deus_ex_machina_count, robbed_caravans_count) 
	FROM '/mnt/dnd_adventures.csv'
	WITH DELIMITER ';'
	CSV header;

COPY "adventure"
	TO '/mnt/dnd_adventures.csv'
	WITH DELIMITER ';'
	CSV header;




