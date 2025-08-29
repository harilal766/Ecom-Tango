from django.test import TestCase
from django.contrib.auth.models import User
from unittest import skip
import json, logging

logger = logging.getLogger()
logger.level = logging.DEBUG


with open("test_data.json", "r") as creds_file:
    test_data_json = json.load(creds_file)
    
    test_user_creds = test_data_json["user"]
    test_username = test_user_creds["username"]
    test_password = test_user_creds["password"]

# Create your tests here.
class TestUser(TestCase):
    def setUpUser(self):
        self.test_user = User.objects.create(**test_user_creds)
        
    @skip("unknown issue")
    def test_get_user(self):
        test_user = User.objects.get(username=test_username)
        self.assertEqual(test_user.username, test_username)