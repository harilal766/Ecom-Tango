from amazon.tests.test_models import *
from amazon.views import SpapiBase, SpapiOrderClient, SpapiReportClient, generatable_amazon_report_types,amazon_reports_trial
from pprint import pprint
from utils import iso_8601_timestamp, iso_8601_converter

from sp_api.base.reportTypes import ReportType
import pandas as pd
from unittest import skip
from dashboard.d_models import ReportProfile
from unittest import skip

import logging
logger = logging.getLogger(__name__)


class Test_SpapiBase(TestSpapiCredential):
    def setUp(self):
        super(Test_SpapiBase,self).setUp()
        self.test_credentials = self.spapi_inst.get_credentials()

        self.few_days_ago = iso_8601_timestamp(-3)
        self.today = iso_8601_timestamp(0)
        self.tomorrow = iso_8601_timestamp(1)
        
    def test_credentials(self):
        self.assertEqual(type(self.test_credentials), dict)
        
    def test_timestamps(self):
        stamps = [self.few_days_ago, self.today, self.tomorrow]
        for stamp in stamps:
            self.assertIsNotNone(stamp)
            self.assertIn('T', stamp)
        
class Test_SpapiOrderClient(Test_SpapiBase):
    def setUp(self):
        super(Test_SpapiOrderClient,self).setUp()
        self.test_api_model = SpapiOrderClient(credentials=self.test_credentials)
        self.ship_date = '2025-12-06T18:29:59Z'
        self.payment_method = ['COD']
        self.order_status = ['Shipped']
        
    #@skip("")
    def test_get_all_orders(self):
        orders_list = self.test_api_model.get_all_orders(
            CreatedAfter = self.few_days_ago,
            LatestShipDate = self.ship_date
        ) 
        #logging.info(orders, self.few_days_ago)
        self.assertEqual(type(orders_list),list)
        self.assertGreater(len(orders_list), 1)
        
    @skip("")
    def test_get_order_ids(self):
        ids = self.test_api_model.get_order_ids(
            CreatedAfter = self.few_days_ago,
            LatestShipDate = self.ship_date,
            PaymentMethods = self.payment_method
        )
        print(ids)
        self.assertEqual(type(ids),list)
        self.assertGreater(len(ids), 1)
        
    @skip("")
    def test_get_shipping_dates(self):
        dates = self.test_api_model.get_shipping_dates()
        self.assertGreater(len(dates),1)
        self.assertEqual(True, self.ship_date in dates)
        
    @skip("")
    def test_get_order_df(self):
        order_df = self.test_api_model.get_order_df(
            CreatedAfter=iso_8601_timestamp(4),
            LatestShipDate = self.ship_date
        )
        self.assertIsNotNone(order_df)
        
class Test_SpapiReportClient(Test_SpapiBase):
    def setUp(self):
        super(Test_SpapiReportClient,self).setUp()
        self.test_api_model = SpapiReportClient(credentials=self.test_credentials)
    
    #@skip("")
    def test_report_id_and_df(self):
        # Working report types
        for key,value in generatable_amazon_report_types.items():
            id = self.test_api_model.create_report_id(
                reportType=value,
                dataStartTime = self.few_days_ago
                #dataEndTime=iso_8601_timestamp(0)
            )
            print(id)
            self.assertEqual(id.isdigit(), True)

            df = self.test_api_model.create_report_df(reportId=id)
            self.assertIsNotNone(df)