import yaml
import json
from datetime import datetime
import pymysql as mc

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
    query = "SELECT * FROM " + str(config['table_name'])
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


