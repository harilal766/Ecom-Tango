from ..d_models import StoreProfile
from authorization.tests.test_user import TestUser, json_testdata
# Create your tests here.

class TestStoreProfile(TestUser):
    def setUp(self):
        super(TestStoreProfile, self).setUp()
        self.store = StoreProfile.objects.create(
            {"user" : self.test_user,**json_testdata["store"]}
        )
        self.assertTrue(self.store.exists())
        
    def test_platform(self):
        self.assertIn(
            self.store.platform, ["Amazon","Shopify"]
        )