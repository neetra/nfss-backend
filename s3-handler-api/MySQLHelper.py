from Files import File, UserFile
def getFiles(results : File):
    allfiles = []
    
    for i in results:          
            file_obj = {
                "file_key":i[0],
                "file_id": i[1],
                "file_name" : i[2],              
                "file_description":i[3],
                "file_created_at" : i[4],
                "file_modified_at" : i[5],
                                
            } 
            allfiles.append(file_obj)
    return allfiles    

def getFilesWithUser(results : UserFile):
    allfiles = []
    for i in results:
        
            file_obj = {
                "user_id": i[0],
                "user_email": i[1],
                "user_first_name": i[2],
                "user_last_name" : i[3],
                "file_id": i[4],
                "file_key":i[5],
                "file_name" : i[6],           
                "file_description":i[7],
                "file_created_at" : i[8],
                "file_modified_at" : i[9]              
                
            } 
            allfiles.append(file_obj)               
      
    return allfiles      

def closeMysqlconnection(mysql_db, my_cursor):
    if mysql_db.is_connected():
            mysql_db.close()            
            my_cursor.close()
            print("MySQL connection is closed")

