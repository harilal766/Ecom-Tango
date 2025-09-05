from django.shortcuts import render

from dashboard.d_models import StoreProfile
from .models import SpapiCredential

from sp_api.api import Orders, ReportsV2
from sp_api.base.reportTypes import ReportType
from sp_api.base.marketplaces import Marketplaces

from utils import iso_8601_converter, iso_8601_timestamp


permitted_amazon_report_types = {
    "Order Report" : ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL,
    "Return Report" : ReportType.GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE,
    "Settlement Report" : ReportType.GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2
}

permitted_amazon_order_types = [
    "Unshipped", "Shipped"
]


# Create your views here.
class SpapiBase:
    def __init__(self,credentials:dict):
        self.credentials = credentials

class SpapiOrderClient(SpapiBase):
    def __init__(self,credentials:dict):
        super().__init__(credentials=credentials)
        self.api_model = Orders(
            credentials=self.credentials,
            marketplace=Marketplaces.IN
        )

class SpapiReportClient(SpapiBase):
    def __init__(self,credentials:dict):
        super().__init__(credentials=credentials)
        self.api_model = ReportsV2(
            credentials=self.credentials,
            marketplace=Marketplaces.IN
        )
    
    def create_report_id(self,reportType,dataStartTime):
        id = None
        try:
            report_details = self.api_model.create_report(
                reportType = reportType,
                dataStartTime = dataStartTime
            )
            return report_details
        except Exception as e:
            print(e)
            
    def get_report_df(self):
        try:
            pass
        except Exception as e:
            print(e)
