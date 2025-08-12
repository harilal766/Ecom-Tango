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