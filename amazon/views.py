from django.shortcuts import render

from dashboard.d_models import StoreProfile
from .models import SpapiCredential

from sp_api.api import Orders, ReportsV2
from sp_api.base.reportTypes import ReportType
from sp_api.base.marketplaces import Marketplaces

from utils import iso_8601_converter, iso_8601_timestamp
import pandas as pd 
import time, requests

from io import StringIO, BytesIO

permitted_amazon_report_types = {
    "Order Report" : ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL,
    "Return Report" : ReportType.GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE
    #"Settlement Report" : ReportType.GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2
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
        
    def get_order_ids(self,**kwargs):
        ids = []
        try:
            orders = self.api_model.get_orders(**kwargs)
            orders = orders.payload.get("Orders")
            for order in orders:
                id = order["AmazonOrderId"]
                if not id in ids:
                    ids.append(id)
        except Exception as e:
            print(e)
        else:
            return ids
    
    def get_order_df(self,**kwargs):
        df = None
        try:
            orders = self.api_model.get_orders(**kwargs)
            orders = orders.payload.get("Orders")
            df = pd.DataFrame(orders)
        except Exception as e:
            print(e)
        else:
            return df 

class SpapiReportClient(SpapiBase):
    def __init__(self,credentials:dict):
        super().__init__(credentials=credentials)
        self.api_model = ReportsV2(
            credentials=self.credentials,
            marketplace=Marketplaces.IN
        )
    
    def create_report_id(self,reportType,dataStartTime,dataEndTime):
        id = None
        try:
            report_details = self.api_model.create_report(
                reportType = reportType,
                dataStartTime = dataStartTime,
                dataEndTime = dataEndTime 
            )
            if report_details:
                id = report_details.payload.get("reportId")
        except Exception as e:
            print(e)
        else:
            return id
            
    def get_report_df(self,reportId = None,reportDocumentId = None):
        df = None
        try:
            if reportId  and reportDocumentId == None:
                while True:
                    report_details = self.api_model.get_report(reportId=reportId)
                    report_status = report_details.payload.get("processingStatus")
                    time.sleep(10)
                            
                    print(report_status)
                            
                    if report_status == "DONE":
                        doc_id = report_details.payload.get('reportDocumentId')
                        report_url = self.api_model.get_report_document(
                            reportDocumentId=doc_id
                        ).payload.get('url')
                                
                        df = pd.read_csv(
                            StringIO(requests.get(report_url).text),
                            sep = '\t'
                        )

                        break
                    elif report_status == 'CANCELLED':
                        df = "cancel"
                        break
        except Exception as e:
            print(e)
        else:
            return df 
