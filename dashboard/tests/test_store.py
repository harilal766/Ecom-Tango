from django.test import TestCase
from ..d_models import BaseCredential, StoreProfile
from authorization.tests.test_user import TestUser, test_data_json
# Create your tests here.

class TestStoreProfile(TestUser):
    def setUp(self):
        self.test_store = StoreProfile.objects.create(
            user = self.test_user,
            platform = test_data_json["store"]["platform"],
            storename = test_data_json["store"]["storename"],
        )
        