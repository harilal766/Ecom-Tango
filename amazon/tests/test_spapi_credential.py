from django.test import TestCase

from authorization.tests.test_user import test_data_json, testuser_creds, TestUser
from amazon.a_models import SpapiCredential

from dashboard.tests.test_store import TestStoreProfile



# Create your tests here.
class TestSpapiCredential(TestStoreProfile):
    def setUp(self):
        self.test_credential = SpapiCredential.objects.create(
            **{
                "user" : self.test_user, "store" : self.test_store,
               **test_data_json["amazon"]
            }
        )
        self.assertTrue(self.test_credential.exists())
        
    def test_report(self):
        report_id = 0
        