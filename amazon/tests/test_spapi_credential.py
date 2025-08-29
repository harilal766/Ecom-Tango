from django.test import TestCase

from authorization.tests.test_user import json_testdata, TestUser
from amazon.a_models import SpapiCredential

from dashboard.tests.test_store import TestStoreProfile


# Create your tests here.
class TestSpapiCredential(TestStoreProfile):
    def setUp(self):
        super(TestSpapiCredential,self).setUp()
        self.test_credential = SpapiCredential.objects.create(
            **{
                "user" : self.test_user, "store" : self.store,
               **json_testdata["amazon"]
            }
        )
        self.assertIsNotNone(self.test_credential)
        
    def test_report_client(self):
        report_id = 0
        