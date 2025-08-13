from django.shortcuts import render, redirect
from amazon.a_models import *
from shopify.models import *
from dashboard.d_models import StoreProfile
from datetime import datetime

# Create your views here.
def home(request):
    return render(request,'dashboard.html')

def view_store(request):
    return render(request,"dashboard.html")

def add_store(request):
    context = {
        "platforms" : ("Amazon", "Shopify"),
        "error" : None
    }
    storeprofile = None
    new_amazon_store = None
    try:
        if request.method == "POST":
            platform = request.POST.get("platform")
            # verify the store name and create based on it
            storename = request.POST.get("Name of the store")
            store_instance = StoreProfile()
            if not store_instance.is_already_created(storename=storename):
                storeprofile = StoreProfile.objects.create(
                    user = request.user, storename = storename,
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
                elif platform == "Shopify":
                    access_token = request.POST.get("Access Token")
                    store_id = request.POST.get("Storename")
                    
                return redirect('dashboard:home')
        return render(request,"add_store.html", context=context)
    except Exception as e:
        context['error'] = str(e)
        return render(request,"error.html", context=context, status=500)