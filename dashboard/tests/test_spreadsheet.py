from dashboard.tests.test_models import TestStoreProfile
from dashboard.spreadsheet import Spreadsheet
from authorization.tests.test_user import json_testdata

import pandas as pd

from testing_files import *

class TestSpreadsheet(TestStoreProfile):
    def setUp(self):
        super(TestSpreadsheet,self).setUp()
        self.label_paths = json_testdata.get("label_paths",None)
        self.test_class = Spreadsheet(
            store = self.test_store,
            report_df = pd.DataFrame(pd.read_excel(amazon_excel)),
            report_type = "Order Report"
        )
        self.pivot_df = self.test_class.create_pivot_table(
            index = amazon_index,other_columns=amazon_columns
        )
        self.assertIsNotNone(self.test_class)
        
    def test_create_pivot_table(self):
        print(self.pivot_df)
        self.assertIsNotNone(self.pivot_df)
    
    def test_create_rate_dict(self):
        rate_dict = self.test_class.create_rate_dict(pivot_df=self.pivot_df)
        print(rate_dict)
        self.assertIsNotNone(rate_dict)
    
    def test_create_tally_table(self):
        pass