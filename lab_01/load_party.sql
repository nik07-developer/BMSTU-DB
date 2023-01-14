
COPY "party" (adventure_id, character_id) 
	FROM '/mnt/dnd_party.csv'
	WITH DELIMITER ';'
	CSV header;




