CREATE TABLE roles(
   role_id INT AUTO_INCREMENT,
   role_name VARCHAR(50),
   PRIMARY KEY(role_id)
);
Insert into roles(role_id, role_name) VALUES (1, "Administrator");
Insert into roles(role_name) VALUES ("Users");

CREATE TABLE users(
   user_id INT AUTO_INCREMENT,
   first_name VARCHAR(255),
   last_name  VARCHAR(255),
   email VARCHAR(255) UNIQUE NOT NULL,
   password NVARCHAR(255) NOT NULL,
   PRIMARY KEY(user_id, email)
);

CREATE TABLE files(
   file_id INT AUTO_INCREMENT,
   file_key VARCHAR(255) UNIQUE NOT NULL,
   name  VARCHAR(255) NOT NULL,
   description VARCHAR(255),
   created_at TIMESTAMP,
   modified_at TIMESTAMP,
   PRIMARY KEY(file_id, file_key)
);

create table users_role(
user_id INT NOT NULL ,
role_id INT NOT NULL,
CONSTRAINT fk_user_id
    FOREIGN KEY (user_id) 
    REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
CONSTRAINT fk_role_id
FOREIGN KEY (role_id) 
    REFERENCES roles(role_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
PRIMARY KEY(user_id,role_id)        
);

create table users_files(
user_id INT NOT NULL ,
file_id INT NOT NULL,
CONSTRAINT fk_user_files_id
FOREIGN KEY (user_id) 
    REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
        CONSTRAINT fk_file_id
FOREIGN KEY (file_id) 
    REFERENCES files(file_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
PRIMARY KEY(user_id, file_id)
)

