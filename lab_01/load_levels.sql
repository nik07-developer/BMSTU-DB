
COPY "progress" (character_id, class_id, "level") 
	FROM '/mnt/dnd_levels.csv'
	WITH DELIMITER ';'
	CSV header;





