from django.test import TestCase
from django.contrib.auth.models import User
from unittest import skip
import json, logging

from django.test import Client

logger = logging.getLogger()
logger.level = logging.DEBUG

with open("test_data.json", "r") as creds_file:
    json_testdata = json.load(creds_file)




# Create your tests here.
class TestUser(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(**json_testdata["user"])
        self.assertIsNotNone(self.test_user)
        
    @skip("")
    def test_signin(self):
        client = Client()
        response = client.get(
            "login", json_testdata["user"]
        )
        self.assertEqual(response.status_code, 200)
    
    @skip("")
    def test_signout(self):
        pass
    