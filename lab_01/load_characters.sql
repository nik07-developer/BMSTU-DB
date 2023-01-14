
COPY "character" (player_id, "level", is_alive, race, gender, "name", background, alignment)
	FROM '/mnt/dnd_characters.csv'
	WITH DELIMITER ';'
	CSV header;

COPY "character" (id, player_id, "level", is_alive)
	TO '/mnt/dnd_characters.csv'
	WITH DELIMITER ';'
	CSV header;




