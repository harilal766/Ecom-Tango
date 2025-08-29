from django.test import TestCase
from ..d_models import StoreProfile
from authorization.tests.test_user import TestUser, test_data_json
# Create your tests here.

class TestStoreProfile(TestUser):
    def setUpStore(self):
        self.test_store = StoreProfile.objects.create(
            {"user" : self.test_user,**test_data_json["store"]}
        )
        self.assertTrue(self.test_store.exists())