
DELIMITER $$
DROP PROCEDURE IF EXISTS SP_DeleteFile $$
CREATE PROCEDURE SP_DeleteFile(
IN emailId VARCHAR(255),
IN filekey VARCHAR(255)
)
BEGIN
	DECLARE fileid INT;
    DECLARE userid INT;
    
	SELECT user_id INTO userid from users where email = emailId;
	SELECT file_id INTO fileid from files where file_key = filekey LIMIT 1;
    
    DELETE FROM users_files WHERE file_id= fileid AND user_id = userid;
    DELETE FROM files WHERE file_id = fileid;
    
END$$

DELIMITER ;