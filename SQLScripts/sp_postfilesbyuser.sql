DELIMITER $$
DROP PROCEDURE IF EXISTS SP_PostFilesByUser $$
CREATE PROCEDURE SP_PostFilesByUser(
IN emailId VARCHAR(255),
IN filekey VARCHAR(255),
IN file_name VARCHAR(255),
IN file_description VARCHAR(255),
IN created_at TIMESTAMP,
IN modified_at TIMESTAMP
)
BEGIN 
	DECLARE userid INT;
    DECLARE fileid INT;
    SELECT user_id INTO userid from users where email = emailId;
	INSERT INTO files( file_key, name, description, created_at, modified_at) VALUES (filekey, file_name, file_description,created_at, modified_at );

    SELECT file_id INTO fileid from files where file_key = filekey LIMIT 1;

    INSERT INTO users_files(file_id, user_id) VALUES (fileid, userid);
 
				
   
END$$

DELIMITER ;