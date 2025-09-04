import json
from datetime import datetime, timedelta

def iso_8601_converter(date_string:str):
    try:
        timestamp = datetime.strptime(date_string,"%Y-%m-%d")
        return timestamp.isoformat()
    except Exception as e:
        print(e)
        
def iso_8601_timestamp(days):
    return (
        datetime.now()- timedelta(days=days)
    ).isoformat()