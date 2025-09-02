from django.test import TestCase

from authorization.tests.test_user import json_testdata, TestUser
from amazon.models import SpapiCredential

from dashboard.tests.test_models import TestStoreProfile
from sp_api.api import Orders, ReportsV2
from sp_api.base.marketplaces import Marketplaces
from sp_api.base.reportTypes import ReportType
from utils import iso_8601_timestamp

# Create your tests here.
class TestSpapiCredential(TestStoreProfile):
    def setUp(self):
        super(TestSpapiCredential,self).setUp()
        self.spapi_instance = SpapiCredential.objects.create(
            **{
                "user" : self.test_user, "store" : self.store,
               **json_testdata["amazon"]
            }
        )
        self.assertIsNotNone(self.spapi_instance)
        self.assertIsNotNone(self.spapi_instance.get_credentials())
        
    def test_are_credentials_verified(self):
        self.assertEqual(
            self.spapi_instance.are_credentials_verified(),
            True
        )