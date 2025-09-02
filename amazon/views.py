from django.shortcuts import render

from dashboard.d_models import StoreProfile
from .models import SpapiCredential

from sp_api.api import ReportsV2
from sp_api.base.reportTypes import ReportType
from sp_api.base.marketplaces import Marketplaces

from utils import iso_8601_converter, iso_8601_timestamp


permitted_amazon_report_types = {
    "Order Report" : ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL,
    "Return Report" : ReportType.GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE
}


# Create your views here.
class SpapiBase:
    def __init__(self,credentials):
        self.credentials = credentials

class SpapiOrderClient(SpapiBase):
    def orders(self):
        try:
            pass
        except Exception as e:
            print(e)
            
            
class SpapiReportClient(SpapiBase):
    def __init__(self,credentials, report_type, starting_date:str, ending_date:str):
        super().__init__(credentials=credentials)
        self.client = ReportsV2(
            credentials= self.credentials,
            marketplace=Marketplaces.IN
        )
        self.report_type = report_type
        self.from_date = iso_8601_converter(date_string=starting_date)
        self.to_date = iso_8601_converter(date_string=ending_date)
    
    def get_report_id(self,report_type):
        try:
            report_details = self.client.create_report(
                ReportType = report_type,
                dataStartTime = self.from_date
            )
            return report_details
        except Exception as e:
            print(e)
            
    def get_report_df(self):
        try:
            pass
        except Exception as e:
            print(e)
