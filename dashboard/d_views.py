from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, FileResponse
# Amazon
from amazon.models import *
from amazon.views import *
from amazon.views import SpapiReportClient
# Shopify
from shopify.sh_models import *
# Dashboard
from dashboard.d_models import StoreProfile,ReportProfile
from datetime import datetime

from utils import iso_8601_converter
from sp_api.api import Orders
from datetime import datetime, timedelta
import pandas as pd
import openpyxl
from io import StringIO, BytesIO

class Dashboard:
    def __init__(self):
        self.supported_platforms = ("Amazon", "Shopify")
        self.platform_specific_datas = {
            "Amazon" : {
                "order_types" : ("Pending","Unshipped", "Shipped"),
                "report_types" : generatable_amazon_report_types
            },
            "Shopify" : {
                "order_types" : ("unfulfilled","fulfilled"),
                "report_types" : ("Order","Return")
            }
        }
# Create your views here.
def home(request):
    try:
        print(request.user.is_superuser)
        if request.user.is_authenticated:
            first_store = StoreProfile.objects.filter(user = request.user).first()
            if first_store:
                store_instance = Store()
                return store_instance.get(request=request, store_slug=first_store.slug)
            else:
                return render(request,"dashboard.html")
        else:
            return render(request,'home.html')
    except Exception as e:
        return HttpResponse(e)

class Store(Dashboard, View):
    def get(self,request,store_slug):
        context = {
            "user" : request.user.username.capitalize(),
            "stores" : StoreProfile.objects.filter(user=request.user),
            "selected_store" : None,
            "order_types" : None, "report_types" : None,
            "settlements" : None,
            "shipping_dates" : None
        }
        try:
            selected_store = StoreProfile.objects.get(user=request.user,slug=store_slug)
            if selected_store.platform == "Amazon":
                spapi_inst = SpapiCredential.objects.get(user = request.user, store = selected_store)
                report_client = SpapiReportClient(credentials=spapi_inst.get_credentials()).api_model
                order_client = SpapiOrderClient(credentials=spapi_inst.get_credentials())
                
                context["settlements"] = report_client.get_reports(
                    reportTypes = ReportType.GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2
                ).payload.get("reports")
                
                # store report columns to use later
                
                
                
                context["shipping_dates"] = order_client.get_shipping_dates()
                
            context["selected_store"] = selected_store
            context["order_types"] = self.platform_specific_datas[selected_store.platform]["order_types"]
            context["report_types"] = self.platform_specific_datas[selected_store.platform]["report_types"]
            
            return render(request,'dashboard.html',context = context)
        except Exception as e:
            return HttpResponse(e)

    def post(self,request):
        context = {
            "platforms" : self.supported_platforms,
            "error" : None
        }
        new_store = None
        try:
            if request.method == "POST":
                platform = request.POST.get("platform")
                # verify the store name and create based on it
                storename = request.POST.get("Name of the store")
                store_instance = StoreProfile()
                if not store_instance.is_already_created(storename=storename):
                    storeprofile = StoreProfile.objects.create(
                        user = request.user, storename = storename,
                        platform = platform,
                        created_date = datetime.now()
                    )
                    storeprofile.save()
                    
                    if platform == "Amazon":
                        new_amazon_store = SpapiCredential.objects.create(
                            user = request.user, store = storeprofile,
                            
                            client_id = request.POST.get("Client Id"),
                            client_secret = request.POST.get("Client Secret"),
                            refresh_token = request.POST.get("Refresh Token")
                        )
                        new_amazon_store.save()
                        new_store = new_amazon_store
                    elif platform == "Shopify":
                        new_shopify_store = ShopifyApiCredential.objects.create(
                            user = request.user, store = storeprofile,
                            storename = request.POST.get("Storename"),
                            access_token = request.POST.get("Access Token")
                        )
                        new_shopify_store.save()
                        new_store = new_shopify_store
                    return home(request)
                
            return render(request,"add_store.html", context=context)
        except Exception as e:
            context['error'] = str(e)
            return render(request,"error.html", context=context, status=500)
    

class StoreReport(View):
    def get(self,request,store_slug,report_id):
        report_df = None
        try:
            selected_store = StoreProfile.objects.get(user=request.user,slug=store_slug)
            if selected_store.platform == "Amazon" :
                spapi_inst = SpapiCredential.objects.get(user = request.user, store = selected_store)
                report_client = SpapiReportClient(credentials=spapi_inst.get_credentials())
                report_df = report_client.create_report_df(reportId=report_id)
        except Exception as e:
            print(e)
        else:
            if report_df:
                buffer = BytesIO()
                report_df.to_excel(buffer,sheet_name='Report', index=False, engine = 'openpyxl')
                buffer.seek(0)
                response = HttpResponse(
                    buffer,
                    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename = settlement : .xlsx'
                return response
    
    def post(self,request,store_slug,ship_date=None):
        report_df = None; pivot_df = None; tally_df = None 
        report_client = None;  pivot = True
        try:
            if request.method == "POST":
                selected_store = StoreProfile.objects.get(user=request.user,slug=store_slug)
                
                selected_report_type = request.POST.get("report-type")
                pivot_table = request.POST.get("pivot_table"); tally_table = request.POST.get("tally_table")
                
                from_date = request.POST.get("from"); to_date = request.POST.get("to")
                print(f"Request datas : {request.POST}")
                
                
                if selected_store.platform == "Amazon":
                    spapi_inst = SpapiCredential.objects.get(user = request.user, store = selected_store)
                    report_client = SpapiReportClient(credentials=spapi_inst.get_credentials())
                    
                    order_client = SpapiOrderClient(credentials=spapi_inst.get_credentials())
                    
                    report_id = report_client.create_report_id(
                        reportType = generatable_amazon_report_types[selected_report_type],
                        dataStartTime = iso_8601_converter(from_date),
                        dataEndTime = iso_8601_converter(to_date)
                    )
                    report_df = report_client.create_report_df(
                        reportId=report_id
                    )
                    
                    if selected_report_type == "Order Report":
                        shipping_date = request.POST.get("shipping_date")
                        method = request.POST.get("payment_method")
                        order_ids  = order_client.get_order_ids(
                            CreatedAfter = from_date,
                            CreatedBefore = to_date,
                            LatestShipDate = shipping_date,
                            PaymentMethod = method
                        )
                        
                        report_df = report_df[
                            report_df["amazon-order-id"].isin(order_ids)
                        ]
                    
                elif selected_store.platform == "Shopify":
                    pass
                if report_df is not None:
                    
                    selected_columns = request.POST.getlist("report_column")
                    if len(selected_columns) > 0:
                        report_df = report_df[selected_columns]
                    
                    print(f"Selected : \n{report_df}")
                    
                    sheets = (
                        {"Name" : "Report", "Content" : report_df},
                        {"Name" : "Pivot Table", "Content" : pivot_df},
                        {"Name" : "Tally Table", "Content" : tally_df}
                    )
                    print(sheets)
                    response = HttpResponse( 
                        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    response['Content-Disposition'] = f'attachment; filename = {selected_report_type} : {from_date} - {to_date}.xlsx'
                    
                    report_profile_handling = ReportProfile.objects.get(
                        user = request.user, store = selected_store,
                        sub_section = generatable_amazon_report_types[selected_report_type]
                    )
                    
                    print(report_profile_handling)
                    
                    with pd.ExcelWriter(response, engine='openpyxl') as writer:
                        report_df.to_excel(writer,index=False,sheet_name="Report")
                        
                        for sheet in sheets:
                            if sheet["Content"] is not None:
                                sheet["Content"].to_excel(writer,index=False,sheet_name = sheet["Name"])
                            
                    return response
        except Exception as e:
            print(e)
            return HttpResponse(e)
        
class Order(View):
    def post(self,request,store_slug):
        try:
            if request.method == "POST":
                selected_store = StoreProfile.objects.get(slug=store_slug)
                credentials = SpapiCredential.objects.get(user = request.user,store = selected_store)
                order_client = Orders(
                    credentials=dict(
                        refresh_token = credentials.refresh_token,
                        lwa_app_id = credentials.client_id,
                        lwa_client_secret = credentials.client_secret
                    ),
                    marketplace=Marketplaces.IN
                )
                
                orders = order_client.get_orders()
                return HttpResponse(orders)
        except Exception as e:
            return HttpResponse(e)