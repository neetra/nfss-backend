DELIMITER $$
DROP PROCEDURE IF EXISTS SP_GetAllFilesByUser $$
CREATE PROCEDURE SP_GetAllFilesByUser()
BEGIN
	SELECT u.user_id, u.email, u.first_name, u.last_name, f.file_id, f.file_key, f.name, f.description, f.created_at, f.modified_at from
users_files uf INNER  JOIN  users u ON u.user_id = uf.user_id 
INNER JOIN files f ON f.file_id = uf.file_id order by u.user_id;
   
END$$

DELIMITER ;