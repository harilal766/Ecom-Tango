from amazon.tests.test_models import *
from amazon.views import SpapiBase, SpapiOrderClient, SpapiReportClient, permitted_amazon_report_types
from pprint import pprint
from utils import iso_8601_timestamp, iso_8601_converter

from sp_api.base.reportTypes import ReportType
import pandas as pd


class Test_SpapiBase(TestSpapiCredential):
    def setUp(self):
        super(Test_SpapiBase,self).setUp()
        self.test_credentials = self.spapi_inst.get_credentials()
        
    def test_credentials(self):
        self.assertEqual(type(self.test_credentials), dict)
        
class Test_SpapiOrderClient(Test_SpapiBase):
    def setUp(self):
        super(Test_SpapiOrderClient,self).setUp()
        self.test_api_model = SpapiOrderClient(credentials=self.test_credentials)
        
    def test_get_order_ids(self):
        ids = self.test_api_model.get_order_ids(
            CreatedAfter = iso_8601_converter("2025-09-01"),
            CreatedBefore = iso_8601_converter("2025-09-07"),
            LatestShipDate = '2025-09-08T18:29:59Z',
            PaymentMethod = "Standard" #Standard CashOnDelivery
        )
        self.assertGreater(len(ids),0)
        print(len(ids))
        
    def test_get_shipping_dates(self):
        dates = self.test_api_model.get_shipping_dates()
        self.assertGreater(len(dates),0)
        
    def test_get_order_df(self):
        order_df = self.test_api_model.get_order_df(
            CreatedAfter=iso_8601_timestamp(4),
            LatestShipDate = '2025-09-08T18:29:59Z',
        )
        self.assertIsNotNone(order_df)
        
        
        
class Test_SpapiReportClient(Test_SpapiBase):
    def setUp(self):
        super(Test_SpapiReportClient,self).setUp()
        self.test_api_model = SpapiReportClient(credentials=self.test_credentials)
    
    def test_create_report(self):
        for type in permitted_amazon_report_types:
            if not "settlement" in type.lower(): 
                id = self.test_api_model.create_report_id(
                    reportType=permitted_amazon_report_types[type],
                    dataStartTime=iso_8601_timestamp(5),
                    dataEndTime=iso_8601_timestamp(0)
                )
                self.assertEqual(id.isdigit(), True)
                #df = self.test_api_model.get_report_df(reportId=id)
                