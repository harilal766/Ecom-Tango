from django.shortcuts import render

from dashboard.d_models import StoreProfile
from .models import SpapiCredential

from sp_api.api import Orders, ReportsV2
from sp_api.base.reportTypes import ReportType
from sp_api.base.marketplaces import Marketplaces

from utils import iso_8601_converter, iso_8601_timestamp


permitted_amazon_report_types = {
    "Order Report" : ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL,
    "Return Report" : ReportType.GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE
}

permitted_amazon_order_types = [
    "Unshipped", "Shipped"
]


# Create your views here.
class SpapiBase:
    def __init__(self,credentials:dict,Api_Model):
        self.credentials = credentials
        self.api_model = Api_Model
        self.client = Api_Model(
            credentials = self.credentials,
            marketplace = Marketplaces.IN
        )

class SpapiOrderClient(SpapiBase):
    def __init__(self,credentials:dict,Api_Model):
        super().__init__(credentials=credentials,Api_Model=Api_Model)

class SpapiReportClient(SpapiBase):
    def __init__(self,credentials:dict,Api_Model):
        super().__init__(credentials=credentials,Api_Model=Api_Model)
    
    def get_report_id(self,report_type):
        try:
            report_details = self.client.create_report(
                ReportType = report_type,
                dataStartTime = self.starting_date
            )
            return report_details
        except Exception as e:
            print(e)
            
    def get_report_df(self):
        try:
            pass
        except Exception as e:
            print(e)
