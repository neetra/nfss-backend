DELIMITER $$
DROP PROCEDURE IF EXISTS SP_GetFilesByUser $$
CREATE PROCEDURE SP_GetFilesByUser(
IN emailId VARCHAR(255)
)
BEGIN
	DECLARE userId INT DEFAULT 0 ;
    
    SELECT user_id 
    INTO userId
    FROM users where email = emailId ;    

    select  file_key, file_id, name, description, created_at, modified_at  from files where file_id IN (
		select file_id from users_files where user_id = userId
    );   
   
END$$

DELIMITER ;