import sqlitecloud, json

def get_remote_db(json_file):
    try:
        with open(json_file, "r") as creds:
            creds = json.load(creds)
            connection_string = creds["db_connection"]
    except Exception as e:
        print(e)
    else:
        return connection_string
    
    
from datetime import datetime

def iso_8601_converter(date_string):
    try:
        timestamp = datetime.strptime(date_string,"%Y-%m-%d")
        return timestamp.isoformat()
    except Exception as e:
        print(e)