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
    def __init__(
        self,user, selected_store,starting_timestamp, ending_timestamp
    ):
        self.credentials = SpapiCredential.get_credentials(
            user=user, store_slug=selected_store.slug
        )
        self.starting_timestamp = starting_timestamp,
        self.ending_timestamp = ending_timestamp
        
class SpapiOrderClient(SpapiBase):
    def orders(self):
        try:
            pass
        except Exception as e:
            print(e)
        
        
class SpapiReportClient(SpapiBase):
    def __init__(self,report_type):
        super().__init__()
        self.client = ReportsV2(
            credentials= self.credentials,
            marketplace=Marketplaces.IN
        )
        self.report_type = report_type
        self.dataStartTime = iso_8601_timestamp(0)
    
    def get_report_id(self):
        try:
            pass
        except Exception as e:
            print(e)
            
    def get_report_df(self):
        try:
            pass
        except Exception as e:
            print(e)
