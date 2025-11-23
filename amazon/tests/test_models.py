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
        selected_amzn_creds = list(json_testdata['amazon'].keys())[0]
        super(TestSpapiCredential,self).setUp()
        self.spapi_inst = SpapiCredential.objects.create(
            **{
                "user" : self.test_user, "store" : self.test_store,
               **json_testdata["amazon"][selected_amzn_creds]
            }
        )
        self.assertIsNotNone(self.spapi_inst)
        self.assertIsNotNone(self.spapi_inst.get_credentials())
        
    def test_are_credentials_verified(self):
        self.assertEqual(
            self.spapi_inst.are_credentials_verified(),
            True
        )
        
