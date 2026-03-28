import json
from datetime import datetime, timedelta, timezone
from django.utils import timezone

def iso_8601_converter(date_string:str):
    time_string = None
    try:
        timestamp = datetime.strptime(
            date_string,"%Y-%m-%d"
        )
        return timestamp.isoformat()
    except Exception as e:
        print(e)
        
def iso_8601_timestamp(days:int):
    timestamp = datetime.today() + timedelta(days=days)
    #timestamp = timezone.now() + timedelta(days=days)
    if days < 0:
        pass
    elif days > 0:
        pass
    return timestamp.isoformat()