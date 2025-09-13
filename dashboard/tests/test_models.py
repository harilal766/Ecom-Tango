from ..d_models import StoreProfile, ReportProfile
from authorization.tests.test_user import TestUser, json_testdata
# Create your tests here.

class TestStoreProfile(TestUser):
    def setUp(self):
        super(TestStoreProfile, self).setUp()
        self.test_store = StoreProfile.objects.create(
            **{"user" : self.test_user,**json_testdata["store"]}
        )
        self.assertIsNotNone(self.test_store)
        
    def test_platform(self):
        self.assertIn(
            self.test_store.platform, ["Amazon","Shopify"]
        )
        
class TestReportProfile(TestStoreProfile):
    def SetUp(self):
        super(TestReportProfile, self).setUp()
        self.profile = 0