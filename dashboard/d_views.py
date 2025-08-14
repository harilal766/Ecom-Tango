from django.shortcuts import render, redirect
from amazon.a_models import *
from shopify.sh_models import *
from dashboard.d_models import StoreProfile
from datetime import datetime

# Create your views here.
def home(request):
    try:
        if request.user.is_authenticated:
            stores = StoreProfile.objects.filter(user=request.user)
            first_store_slug = stores[0].slug if len(stores) > 0 else None
            return view_store(request,store_slug=first_store_slug)
        else:
            return render(request,'home.html')
    except Exception as e:
        return render(request,"error.html", context={"error" : str(e)})
        
def view_store(request,store_slug):
    context = {
        "user" : None,
        "stores" : None,
        "selected_store" : None
    }
    try:
        if request.user.username == "":
            return render(request,'home.html',context=context)
        else:
            context["user"] = request.user.username.capitalize()
            context["stores"] = StoreProfile.objects.all()
            if store_slug:
                context["selected_store"] = StoreProfile.objects.get(slug = store_slug)
        return render(request,"dashboard.html",context=context)
    except Exception as e:
        return render(request,"error.html",{"error" : e})
    
def add_store(request):
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