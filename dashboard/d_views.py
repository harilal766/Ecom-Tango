from django.shortcuts import render, redirect

# Amazon
from amazon.models import *
from amazon.views import *
# Shopify
from shopify.sh_models import *
# Dashboard
from dashboard.d_models import StoreProfile
from datetime import datetime
from django.views import View
from django.http import HttpResponse

from utils import iso_8601_converter

class Dashboard:
    def __init__(self):
        self.supported_platforms = ("Amazon", "Shopify")
        self.platform_specific_datas = {
            "Amazon" : {
                "order_types" : ("Pending","Unshipped", "Shipped"),
                "report_types" : permitted_amazon_report_types
            },
            "Shopify" : {
                "order_types" : ("unfulfilled","fulfilled"),
                "report_types" : ("Order","Return")
            }
        }


# Create your views here.
def home(request):
    try:
        if request.user.is_authenticated:
            first_store = StoreProfile.objects.filter(user = request.user)[0]
            store_instance = Store()
            return store_instance.get(request=request, store_slug=first_store.slug)
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
            "order_types" : None, "report_types" : None
        }

        try:
            selected_store = StoreProfile.objects.get(user=request.user,slug=store_slug)
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
    
    
from amazon.views import SpapiReportClient
class StoreReport(View):
    def post(self,request,store_slug):
        report_inst = None; report_df = None
        try:
            if request.method == "POST":
                selected_store = StoreProfile.objects.get(user=request.user,slug=store_slug)
                
                selected_report_type = request.POST.get("report-type")
                from_date = request.POST.get("from"); to_date = request.POST.get("to")
                
                if selected_store.platform == "Amazon":
                    spapi_inst = SpapiCredential.objects.get(user = request.user, store = selected_store)
                    report_inst = SpapiReportClient(
                        credentials=spapi_inst.get_credentials(),
                        starting_date = from_date,ending_date=to_date
                    )
                    selected_report_type = permitted_amazon_report_types[selected_report_type]
                    report_df = report_inst.get_report_id(
                        report_type=selected_report_type
                    )
                    print(report_df)
                elif selected_store.platform == "Shopify":
                    pass
                
                return HttpResponse(report_df)
        except Exception as e:
            print(e)
            return HttpResponse(e)
        
from sp_api.api import Orders
from datetime import datetime, timedelta

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