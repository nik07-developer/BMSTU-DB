
COPY "death" (character_id, death_reason, last_words, "date") 
	FROM '/mnt/dnd_deaths.csv'
	WITH DELIMITER ';'
	CSV header;





