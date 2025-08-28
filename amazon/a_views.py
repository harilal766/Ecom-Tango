from django.shortcuts import render

from dashboard.d_models import StoreProfile
from .a_models import SpapiCredential
from sp_api.base.reportTypes import ReportType


permitted_amazon_report_types = {
    "Order Report" : ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL,
    "Return Report" : ReportType.GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE
}


def get_spapi_credentials(request,store_slug):
    try:
        amazon_store = StoreProfile.objects.get(user= request.user, slug = store_slug)
        credential_instance = SpapiCredential.objects.get(request.user,store=amazon_store)
        return credential_instance
    except Exception as e:
        print(e)


# Create your views here.
