from dashboard.tests.test_models import TestStoreProfile
from dashboard.spreadsheet import Spreadsheet
from authorization.tests.test_user import json_testdata

from authorization.tests.test_user import json_testdata
class TestSpreadsheet(TestStoreProfile):
    def setUp(self):
        super(TestSpreadsheet,self).setUp()
        self.label_paths = json_testdata.get("label_paths",None)
        self.test_class = Spreadsheet(
            store = self.test_store,
            report_df = None, 
            report_type = "Order Report"
        )
        self.assertIsNotNone(self.test_class)
    
    def test_create_tally_table(self):
        for platform,path in self.label_paths.items():
            self.assertIsNotNone(path)
            
            tally_table = self.test_class.create_tally_table(
                label_path = path, pivot_df=None
            )
            print(tally_table)
            self.assertIsNotNone(tally_table)