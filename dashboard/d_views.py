from django.shortcuts import render, redirect
from amazon.a_models import *
from shopify.sh_models import *
from dashboard.d_models import StoreProfile
from datetime import datetime
from django.views import View

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
        return render(request,"error.html", context={"error" : str(e)})

class Store(View):
    def get(self,request,store_slug):
        context = {
            "user" : request.user.username.capitalize(),
            "stores" : StoreProfile.objects.filter(user=request.user),
            "order_types" : None, "report_types" : None
        }
        platform_specific_data = {
            "Amazon" : {
                "order_types" : ("Pending","Unshipped", "Shipped"),
                "report_types" : ("Order","Settlement")
            },
            "Shopify" : {
                "order_types" : ("unfulfilled","fulfilled"),
                "report_types" : ("Order","Return")
            }
        }
        try:
            selected_store = StoreProfile.objects.get(user=request.user,slug=store_slug)
            context["order_types"] = platform_specific_data[selected_store.platform]["order_types"]
            context["report_types"] = platform_specific_data[selected_store.platform]["report_types"]
            
            print(f"Platform : {selected_store.platform}, types : {context['order_types']}")
            return render(request,'dashboard.html',context = context)
        except Exception as e:
            return render(request,"error.html",{"error":e})

    def post(self,request):
        context = {
            "platforms" : ("Amazon", "Shopify"),
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
    
        
    
def get_report(request,store_slug):
    try:
        return render(request,"")
    except Exception as e:
        return render(request,"error.html",{"error":e})