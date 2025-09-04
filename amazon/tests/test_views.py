from amazon.tests.test_models import *
from amazon.views import SpapiBase, SpapiOrderClient
from pprint import pprint


class Test_SpapiBase(TestSpapiCredential):
    def setUp(self):
        super(Test_SpapiBase,self).setUp()
        self.test_credentials = self.spapi_inst.get_credentials()
        self.starting_date = "2025-09-03",
        self.ending_date = "2025-09-03"

        self.assertEqual(type(self.test_credentials), dict)
        
class Test_SpapiOrderClient(Test_SpapiBase):
    def setUp(self):
        super(Test_SpapiOrderClient,self).setUp()
        self.test_api_model = SpapiOrderClient(
            credentials=self.test_credentials,
            model=Orders
        )