from ..d_models import StoreProfile, ReportProfile, BaseCredential
from authorization.tests.test_user import TestUser, json_testdata
# Create your tests here.

class TestStoreProfile(TestUser):
    def setUp(self):
        super(TestStoreProfile, self).setUp()
        test_stores = json_testdata["stores"]
        for store in test_stores:
            self.test_store = StoreProfile.objects.create(
                **{"user" : self.test_user,**store}
            )
            self.assertIsNotNone(self.test_store)
        
    def test_platform(self):
        self.assertIn(
            self.test_store.platform, ["Amazon","Shopify"]
        )
        

class TestBaseCredential(TestStoreProfile):
    def setUp(self):
        super(TestBaseCredential,self).setUp()
        self.base_credential_instance = BaseCredential()
    """
    def test_get_credential(self):
        self.assertIsNotNone(self.base_credential_instance.get_the_credentials())
    """
class TestReportProfile(TestStoreProfile):
    def SetUp(self):
        super(TestReportProfile, self).setUp()
        self.profile = ReportProfile.objects.get()
        
    