# NFSS Service
NFSS service is REST API, which serves authentication, create new user, upload, edit, view and delete file.
Files are stored in Amazon S3.

# Requirements
| Technology | Version
--- | --- |
| MySql| 8.0.26
| Python| 3.8.0
| zappa (Required for deployment)| 0.54.0|

# AWS Resources

Cloud Deployment Architecture is [here](https://drive.google.com/file/d/120mL-v04F57k35_S9FpJNIjVN69bLTe8/view?usp=sharing).
- Lambda
- API Gateway
- VPC
- Security group to allow inbound rule 3306 for TCP/IP
- RDS MySQL
- S3


# Demo is [here](https://drive.google.com/file/d/1GhkvAWqTPVCtJ1DAej4GfA0gsGB8_U8l/view?usp=sharing)

# Steps to run locally

- Edit [config.py](config.py) and set your credentials.
- Run following command:
    ```
    pip install -r requirements.txt
    flask run
    ```
# Steps to deploy using zappa
Requires python virtual env.
Refer [this](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) to setup python in virtual environment
|Commands| Description
|-|-|
|zappa init| Defines deployment configuration in [zappa_settings.json](zappa_settings.json)
|zappa deploy dev| Deploy application dev stage as per settings in zappa_settings.json
|zappa trail dev| Trace logs. Here dev is stage
|zappa update dev| Deploy updated application to dev stage|


# Test with postman resources 
- [here](https://drive.google.com/drive/folders/1uzqRkrUMuRBnzrDTGT3IxTJVim7-nOdZ?usp=sharing) is the postman collection
- Import the postman collection and environment.
- Set values of url and token.
- Refer demo video