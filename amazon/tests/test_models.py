from django.test import TestCase

from authorization.tests.test_user import json_testdata, TestUser
from amazon.amzn_models import SpapiCredential

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
        ).get_credentials()
        self.assertIsNotNone(self.spapi_instance)
        
    def test_report_client(self):
        spapi_credentials = self.spapi_instance.get_credentials(
            user=self.test_user,store_slug=self.store.slug
        )
        report_client = ReportsV2(
            credentials= {
                "refresh_token" : spapi_credentials.refresh_token,
                "lwa_app_id" : spapi_credentials.client_id,
                "lwa_client_secret" : spapi_credentials.client_secret    
            },
            marketplace=Marketplaces.IN
        )
        
        report_id = report_client.create_report(
            reportType = ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL,
            dataStartTime = iso_8601_timestamp(7)
        )
        
        print(report_id)