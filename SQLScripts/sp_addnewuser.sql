
DELIMITER $$
DROP PROCEDURE IF EXISTS SP_AddNewUser $$
CREATE PROCEDURE SP_AddNewUser(
IN emailId VARCHAR(255),
IN firstname VARCHAR(255),
IN lastname VARCHAR(255),
IN userpassword NVARCHAR(255)
)
BEGIN
	
    DECLARE userid INT;
	INSERT into users(first_name, last_name, email, password) values (firstname, lastname, emailId, userpassword) ;
	SELECT * FROM users where email = emailId;
    
END$$

DELIMITER ;