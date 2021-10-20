from datetime import datetime
class File:
    def __init__(self):
        self.file_name = ""
        self.file_key =""
        self.file_description=""
        self.created_at= datetime.now()
        self.modified_at = datetime.now()
        self.file_id = ""

class UserFile:
    def __init__(self):
        self.file_name = ""
        self.file_key =""
        self.file_description=""
        self.created_at= ""
        self.modified_at = ""
        self.file_id = ""
        self.user_id=" "
        self.email=""
        self.first_name=""
        self.last_name =""     