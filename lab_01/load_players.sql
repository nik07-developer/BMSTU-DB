
COPY "player" (gender, "name", city, birthday) 
	FROM '/mnt/dnd_players.csv'
	WITH DELIMITER ';'
	CSV header;

COPY "player"
	TO '/mnt/dnd_players.csv'
	WITH DELIMITER ';'
	CSV header;




