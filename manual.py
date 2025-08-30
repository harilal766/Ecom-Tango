import json


with open("test_data.json", "r") as creds_file:
    json_testdata = json.load(creds_file)

from sp_api.api import Orders
from sp_api.base import Marketplaces

client = Orders(
    credentials=dict(
        refresh_token = json_testdata["amazon"]["refresh_token"],
        lwa_app_id = json_testdata["amazon"]["client_id"],
        lwa_client_secret = json_testdata["amazon"]["client_secret"]
    ),
    marketplace=Marketplaces.IN
)

print(client.get_order("405-1181345-7106760"))