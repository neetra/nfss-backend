
DELIMITER $$
DROP PROCEDURE IF EXISTS SP_MultipeIN $$
CREATE PROCEDURE SP_MultipeIN(
IN emailId VARCHAR(255),
IN file_key VARCHAR(255),
IN name VARCHAR(255),
IN description VARCHAR(255),
IN created_at TIMESTAMP,
IN modified_at TIMESTAMP
)
BEGIN
	
       
    INSERT INTO files( file_key, name, description, created_at, modified_at) VALUES (file_key, name, description,created_at, modified_at ); 
   SELECT emailId;
   SELECT file_key;
    
END$$

DELIMITER ;