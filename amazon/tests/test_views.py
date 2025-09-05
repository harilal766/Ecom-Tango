from amazon.tests.test_models import *
from amazon.views import SpapiBase, SpapiOrderClient, SpapiReportClient, permitted_amazon_report_types
from pprint import pprint
from utils import iso_8601_timestamp, iso_8601_converter


class Test_SpapiBase(TestSpapiCredential):
    def setUp(self):
        super(Test_SpapiBase,self).setUp()
        self.test_credentials = self.spapi_inst.get_credentials()
        self.starting_date = iso_8601_timestamp(4),
        self.ending_date = iso_8601_timestamp(0)
        
    def test_credentials(self):
        self.assertEqual(type(self.test_credentials), dict)
        
class Test_SpapiOrderClient(Test_SpapiBase):
    def setUp(self):
        super(Test_SpapiOrderClient,self).setUp()
        self.test_api_model = SpapiOrderClient(credentials=self.test_credentials)
        
class Test_SpapiReportClient(Test_SpapiBase):
    def setUp(self):
        super(Test_SpapiReportClient,self).setUp()
        self.test_api_model = SpapiReportClient(credentials=self.test_credentials)
    
    def test_create_report_id(self):
        id = self.test_api_model.create_report_id(
            report_type=permitted_amazon_report_types["Order Report"],
            starting_date=self.starting_date
        )
        print(id)