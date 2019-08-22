import yaml
import json
from datetime import datetime
import pymysql as mc

import boto3
from botocore.exceptions import NoCredentialsError

import mandrill

def send_email(messages):
    mandrill_client = mandrill.Mandrill(mandrill_key)
    try:
        message = {'from_mail': fromEmail,
                    'from_name': name,
                    'to':[{
                        'email': toEmail,
                        'type': 'to',
                    }],
                    'subject': subject,
                    'html': messages,
                    'header': {'X-MC-PreserveRecipients': False}
                    }
        result = mandrill_client.messages.send(message = message)

    except mandrill.Error as e:
        print("Error in sending mail:",e)
    

def upload_to_aws(local_file, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    
    bucket = BUCKET
    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL':'public-read'})
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def result_to_file(results):
    filename = 'query_files/contacts_' + str(datetime.now().strftime('%Y-%m-%d|%H:%M:%S')) + '.txt'
    with open(filename,'w') as file:
        for row in results:
            file.write("%s\n" % str(row))
    return filename

def getDBconnection():
    try:
        cnx = mc.connect(config['database']['host'],config['database']['username'],config['database']['password'],
                        config['database']['db_name'])
        return cnx
    except Exception as e:
        print("Error while connecting to DB: {}".format(e))

def query_return():
    query = "SELECT {name}, {number} FROM {table}".format(table=str(config['table']['name']), number=config['table']['number_column'], name=config['table']['name_column'])
    try:
        where = config['table']['where']
        query = "{query} WHERE {where}".format(where=where, query=query)
    except:
        pass

    cnx = getDBconnection()
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("Error while executing query:{}".format(e))
    return False

def load_config(fname):
    return yaml.load(open(fname))

config = load_config("config.yaml")
input_format = json.loads(config['input_format'])

access_key = config['AWS']['S3']['accessKey']
secret_key = config['AWS']['S3']['secretKey']
bucket = config['AWS']['S3']['bucket']

mandrill_key = config['email']['mandrillKey']
subject = config['email']['subject']
fromEmail = config['email']['from']
toEmail = config['email']['to']
name = config['email']['name']

ACCESS_KEY = access_key
SECRET_KEY = secret_key
BUCKET = bucket

