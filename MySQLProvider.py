from configparser import Error
from typing import Tuple
import mysql.connector 
from Files import File
from MySQLHelper import getFiles, getFilesWithUser, closeMysqlconnection
from datetime import datetime
import config
from Helper import get_time_from_string;
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector.cursor import MySQLCursorDict, MySQLCursorPrepared

class MySQLProvider():   

    def connect_to_db():
        nfss_db=mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database  
        return nfss_db
 
    def getAllFiles(self):
        try:  
            nfss_db =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database  
            
            #Why set dictionary=True? because MySQLCursorDict creates a cursor that returns rows as dictionaries so we can access using column name (here column name is the key of the dictionary)
            my_cursor= nfss_db.cursor(dictionary = True)

            #Execute SQL Query to select all records 
            my_cursor.execute("select file_key,name, description, created_at, modified_at from files")  
            result=my_cursor.fetchall() #fetches all the rows in a result set   
            allfiles =  self.getAllFiles(result)
            
            return (allfiles)            
        except mysql.connector.Error as err:
            print('Error:Unable to fetch data.' , err)  
            nfss_db.rollback()
        finally:
            closeMysqlconnection(nfss_db, my_cursor)     

    def get_all_files_by_user(self):       
        try:   
            nfss_db =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database    
            my_cursor=nfss_db.cursor(dictionary=True) 
      
            my_cursor.callproc('SP_GetAllFilesByUser')
            allFiles = []
            for result in my_cursor.stored_results():
                allFiles = allFiles + getFilesWithUser(result.fetchall())

            return(allFiles)  
        except mysql.connector.Error as err:  
            #rollback used for if any error   
            nfss_db.rollback()  
        finally:
            closeMysqlconnection(nfss_db, my_cursor) 

    def get_files_by_user(self, email):
        try:     
            nfss_db =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database  
            my_cursor=nfss_db.cursor(cursor_class = MySQLCursorDict) 
            args = [email]
            my_cursor.callproc('SP_GetFilesByUser', args)
            allFiles = []
            for result in my_cursor.stored_results():
                a_files=  getFiles(result.fetchall())
                allFiles = allFiles + a_files

            return(allFiles)  
        except mysql.connector.Error as err:  
            #rollback used for if any error   
            nfss_db.rollback()  
        finally:
            closeMysqlconnection(nfss_db, my_cursor) 

    def add_entry_of_file(self, file : File, username)    :
        try:   
            nfss_db =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database     
            my_cursor=nfss_db.cursor()          
            
            my_cursor.callproc('SP_PostFilesByUser', ( username, file.file_key, file.file_name, file.file_description, get_time_from_string(file.created_at),  get_time_from_string(file.modified_at)))
            nfss_db.commit()          
        except mysql.connector.Error as err:  
            #rollback used for if any error   
            nfss_db.rollback()  
        finally:
            closeMysqlconnection(nfss_db, my_cursor)  

    def delete_file(self, file_key, emailId)    :
        try:      
            nfss_db =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database   
            my_cursor=nfss_db.cursor()        
            my_cursor.callproc('SP_DeleteFile', ( emailId, file_key))
            nfss_db.commit()         
        except mysql.connector.Error as err:  
            #rollback used for if any error   
            nfss_db.rollback()  
        finally:
            closeMysqlconnection(nfss_db, my_cursor)                    

    def get_user_by_username_or_id(self, username, userid):
        try: 
            nfss_db =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database   
            my_cursor = nfss_db.cursor(dictionary = True)
            query = "SELECT * FROM users WHERE email=%s or user_id =%s"
        
            tuple1 = (username, userid)
            my_cursor.execute(query, tuple1)
            results = my_cursor.fetchone()
            if(results is None):
                return None
            return results                
        except mysql.connector.Error as err:
            print (err)     
        finally:
            closeMysqlconnection(nfss_db, my_cursor)                   
        
        return None

    def get_sql_version(self):
        try:             
            nfss_db =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database,connect_timeout=10000 )#established connection between your database   
            
            my_cursor = nfss_db.cursor(dictionary = True)
            
            query = "SELECT version()"
        
            
            my_cursor.execute(query)
            
            results = my_cursor.fetchone()
            if(results is None):
                return None
                         
            return results["version()"]               
        except mysql.connector.Error as err:
            print (err)     
        finally:
            closeMysqlconnection(nfss_db, my_cursor)                   
        
        return None
        

    def check_user(self, username, password):
        try: 
            nfss_db =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database   
            my_cursor = nfss_db.cursor(dictionary = True)
            query = "SELECT u.user_id, u.password, u.email, u.first_name, u.last_name, ur.role_id FROM users u LEFT JOIN users_role ur ON u.user_id = ur.user_id  WHERE email = %s"
        
            tuple1 = [username]
            my_cursor.execute(query, tuple1)
            results = my_cursor.fetchone()          
            if(check_password_hash(results['password'], password)):
                return results
            else:
                return None                
        except mysql.connector.Error as err:
            print (err)
        finally:
            closeMysqlconnection(nfss_db, my_cursor)         
        
        return None

    def create_user(self, user_l):
        try:      
            
            nfss_db =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database   
            
            my_cursor=nfss_db.cursor()    
            hash_password = generate_password_hash(user_l["password"])    
            my_cursor.callproc('SP_AddNewUser', (user_l['email'],  user_l['first_name'], user_l['last_name'], hash_password))       
            nfss_db.commit()
            results = my_cursor.stored_results()
            for result in results:
                return result.fetchone()
        except mysql.connector.Error as err:
            print (err)          
            
        finally:
            closeMysqlconnection(nfss_db, my_cursor)  
        return None    
