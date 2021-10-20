import boto3
from botocore.exceptions import NoCredentialsError
import botocore;
from datetime import datetime
import uuid
from mysql.connector.errors import Error
from Files import File
from Constants import project_tag, bucket_name
import config
from helper import create_file_object

class S3Handler:
    def __init__(self):       
        self.session = boto3.Session( aws_access_key_id=config.aws_access_key_id, aws_secret_access_key=config.aws_secret_access_key)
        self.s3_client = self.session.client('s3', 'us-east-2',config=botocore.config.Config(s3={'addressing_style':'path'}))
        #self.s3_client = boto3.client('s3')
        self.s3_resource_tag = {'Key':"resource",'Value':"s3"}
        self.tags = [project_tag, self.s3_resource_tag]

    def addTagsOnBucket(self, bucket_name, key, i_tags):
        self.tags.append(i_tags)
        self.s3_client.put_object_tagging(
                Bucket=bucket_name,
                Key=key,    
                Tagging={
                'TagSet': self.tags
            })  
        self.tags.clear()              

    def delete_file(self, filename):
        try:
           self.s3_client.delete_object(
            Bucket= bucket_name,
            Key= filename)
           return {"message" :"File not present"}           
        except Error as e:
            return {"message" : "Cannot delete file"}       
                     
       
    def get_objects_at(self):        
        obj = self.s3_client.list_objects(Bucket = "nfss-primary" )
        return obj;
    def upload_file(self, local_file, email):
        try:            
            file = create_file_object(local_file)
            # upload file to s3 bucket
            self.s3_client.upload_file(local_file, 
                        bucket_name,
                        file.file_key,
                        ExtraArgs = 
                                {'Metadata':
                                    {
                                        'description': file.file_description, 
                                        'name': file.file_name, 
                                        'CreatedAt' : file.created_at, 
                                        'ModifiedAt' : file.modified_at,
                                        'username' : email
                                    }})
        
            self.addTagsOnBucket(bucket_name, file.file_key, {'Key' : 'object-name', 'Value' :file.file_key})       
        
            print("Upload Successful")
            return file;
        except FileNotFoundError:
            print("The file was not found")
            return None
        except NoCredentialsError:
            print("Credentials not available")
            return None

    def get_objects(self, path):
        for obj in self.s3_client.list_objects(Bucket= "userfilesfirstorigin")['Contents']:
            print (obj)
