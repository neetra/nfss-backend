from configparser import Error
from logging import error
from flask import Flask, request, current_app
from flask_jwt import JWT, jwt_required
from Files import UserFile
from MySQLProvider import MySQLProvider
from datetime import datetime
from secrets import token_urlsafe;
from S3Handler import S3Handler;
import os, sys;
from flask_cors import CORS
import os, tempfile, zipfile

mysqlprovider = MySQLProvider()
s3_handler = S3Handler()
class User(object):
    def __init__(self, user_id, email, first_name, last_name, role_id =2):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.role_id = role_id
    def __str__(self):
        return "User(id='%s')" % self.id

def make_payload(identity):  
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    return {
        'exp': exp, 'iat': iat, 'nbf': nbf,
        'user_id': identity.user_id,
        'role_id' : identity.role_id,
        'first_name' : identity.first_name,
        'last_name': identity.last_name,
        'email': identity.email,
        'service':'nfss'
        }  

def authenticate(username, password):
    user = mysqlprovider.check_user(username, password)
    if(user is None):
        return "Unauthorized user"        
    if(user['role_id'] == None)         :
        user['role_id'] =2
                
    return User(user['user_id'], user['email'], user['first_name'], user['last_name'], user['role_id'])

def identity(payload):
    user_id = payload['user_id']
    user = mysqlprovider.get_user_by_username_or_id("", user_id)
    if (user is None):
        return None   

    return user          

app = Flask(__name__)

app.config['SECRET_KEY'] = token_urlsafe(16)  
cors = CORS(app)
jwt = JWT(app, authenticate, identity)
jwt.jwt_payload_callback = make_payload

@app.route('/create-user',  methods = ["POST"])
def create_user():
     print("create a user")
     json_data = request.get_json()  
     print(json_data)     
     user  = mysqlprovider.create_user(json_data)
     
     if user is None:
         return "Bad request either username exist or password not valid",400
     else:
         return "User is created", 200

def get_role_id(token):     
    decoded_token = decode_token(token)
    role_id =  decoded_token['role_id']
    return role_id

def get_email(token):     
    decoded_token = decode_token(token)
    return decoded_token['email']    

def decode_token(token)   :      
    try:          
        token = token.split(" ")[1]
        decode = jwt.jwt_decode_callback(token)
        return decode;
    except error as e:
        return e        
    
def getTokenFromAuthorizationHeader():
    try:
        token = request.headers["Authorization"]        
        return token
    except:
        return "Error while parsing token"        

@app.route("/createfile", methods = ["POST"])
@jwt_required()
def create_a_file():  
    try:        
        with tempfile.TemporaryDirectory() as tmpdir:
            print(tmpdir)
        token = request.headers["Authorization"]
        email = get_email(token) ;        
        f = request.files['file_key']        
        tmpdir = os.path.dirname(tmpdir)
        dirname = os.path.join(tmpdir, f.filename)      
        f.save(dirname);        
        file  = s3_handler.upload_file(dirname,email)          
        os.remove(dirname)         
        mysqlprovider.add_entry_of_file(file, email)        
        return "Success", 200
    except Error as err:
        return {"message":err.message},400       

@app.route("/file/<file_key>", methods = ["DELETE"])
@jwt_required()
def delete_a_file(file_key):
    try:
        token = request.headers["Authorization"]
        email = get_email(token) ;   
        file_key = file_key.rstrip()    
        response =  s3_handler.delete_file(file_key)
        mysqlprovider.delete_file(file_key, email)
        return response, 200
    except Error as err:
        return {"message":err.message},400    

@app.route("/files")
@jwt_required()
def getFilesByUser():
    try:
        token = request.headers["Authorization"]           
        role_id = get_role_id(token)
        allFiles=[]
        if(role_id != 1):
            email = get_email(token)  
            allFiles = mysqlprovider.get_files_by_user(email)    
        else:            
            allFiles= mysqlprovider.get_all_files_by_user()        
        return {"Files" : allFiles}, 200
    except Error as e:
        return "Error " + e, 400

@app.route("/ping-check-token")
@jwt_required()
def ping_validity_of_token():
    try:        
        return {"message" : "Success"}, 200
    except Error as e:
        return "Error " + e, 400

@app.route("/ping")
def ping():
    try:           
        return {'message' : 'success'}, 200
    except Error as e:
        return "Error " + e, 400
 
if __name__ == '__main__':
    app.run()