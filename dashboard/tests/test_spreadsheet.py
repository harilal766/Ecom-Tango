from django.test import TestCase
from dashboard.spreadsheet import Spreadsheet
from authorization.tests.test_user import json_testdata


class Test_Spreadsheet(TestCase):
    def setUp(self):
        self.label_path = json_testdata["label_path"]
        self.test_class = Spreadsheet()
    
    def test_create_tally_table(self):
        pass