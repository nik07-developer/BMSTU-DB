COPY "class" ("id", "name", "description") 
	FROM '/mnt/tools/dnd_classes.csv'
	WITH DELIMITER ';'
	CSV header;
