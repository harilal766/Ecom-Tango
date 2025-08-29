from django.test import TestCase
from django.contrib.auth.models import User
from unittest import skip
import json, logging

logger = logging.getLogger()
logger.level = logging.DEBUG


with open("test_data.json", "r") as creds_file:
    test_data_json = json.load(creds_file)
    
    testuser_creds = test_data_json["user"]

# Create your tests here.
class TestUser(TestCase):
    def setUpUser(self):
        self.test_user = User.objects.create_user(**testuser_creds)
        self.assertTrue(self.test_user.exists())
        
    @skip("")
    def test_signin(self):
        self.client.login(**testuser_creds)
        response = self.client.get("login")
        self.assertEqual(response.status_code, 200)
    
    @skip("")
    def test_signout(self):
        pass
    