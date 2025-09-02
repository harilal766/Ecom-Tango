from amazon.tests.test_models import *


class Test_SpapiBase(TestSpapiCredential):
    def setUp(self):
        super(Test_SpapiBase,self).setUp()
        self.assertIsNotNone(self.spapi_cred_inst.get_credentials())

class Test_SpapiReportClient(TestSpapiCredential):
    def setUp(self):
        super(Test_SpapiReportClient,self).setUp()
    
    def test_get_report_id(self):
        pass


