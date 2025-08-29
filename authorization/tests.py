from django.test import TestCase
from django.contrib.auth.models import User
import json

with open("test_data.json", "r") as creds_file:
    creds_json = json.load(creds_file)
    user_creds = creds_json["user"]

# Create your tests here.
class TestUser(TestCase):
    def setUp(self):
        self.user_instance = User.objects.create(
            username = user_creds["username"], password=user_creds["password"]
        )
        
    def test_get_user(self):
        test_user = User.objects.get(username=user_creds["username"])
        self.assertEqual(test_user.username, user_creds["username"])