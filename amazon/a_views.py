from django.shortcuts import render

from dashboard.d_models import StoreProfile
from .a_models import SpapiCredential
from sp_api.base.reportTypes import ReportType


permitted_amazon_report_types = {
    "Order Report" : ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL,
    "Return Report" : ReportType.GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE
}


# Create your views here.
class SpapiBase:
    def __init__(self,user, selected_store):
        self.credentials = SpapiCredential.get_credentials(
            user=user, store_slug=selected_store.slug
        )
        
class SpapiReport(SpapiBase):
    def get_report_id(self):
        try:
            pass
        except Exception as e:
            print(e)
