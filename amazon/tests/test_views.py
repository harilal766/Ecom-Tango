from amazon.tests.test_models import *
from amazon.views import SpapiBase, SpapiOrderClient, SpapiReportClient, permitted_amazon_report_types
from pprint import pprint
from utils import iso_8601_timestamp, iso_8601_converter

from sp_api.base.reportTypes import ReportType


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
        
    def test_get_order_df(self):
        order_df = self.test_api_model.get_order_df(
            CreatedAfter=iso_8601_timestamp(4)
        )
        
        order_ids =  order_df["AmazonOrderId"].to_list()
        ship_dates = []
        for id in order_ids:
            row = order_df.loc[order_df['AmazonOrderId'] == id]
            ship_dates.append(row["LatestShipDate"].to_string(index=False))
        print(ship_dates)
        
class Test_SpapiReportClient(Test_SpapiBase):
    def setUp(self):
        super(Test_SpapiReportClient,self).setUp()
        self.test_api_model = SpapiReportClient(credentials=self.test_credentials)
    
    def test_create_report_id(self):
        for type in permitted_amazon_report_types:
            if not "settlement" in type.lower(): 
                id = self.test_api_model.create_report_id(
                    reportType=permitted_amazon_report_types[type],
                    dataStartTime=iso_8601_timestamp(5),
                    dataEndTime=iso_8601_timestamp(0)
                )
                
                self.assertEqual(id.isdigit(), True)