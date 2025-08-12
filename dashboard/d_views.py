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
        "platforms" : ("Amazon", "Shopify")
    }
    try:
        if request.method == "POST":
            platform = request.POST.get("platform")
            
            # verify the store name and create based on it
            storename = request.POST.get("Name of the store")
            
            store_instance = StoreProfile()
            if not store_instance.is_already_created(storename=storename):
                new_store = StoreProfile.objects.create(
                    storename = storename, platform = platform, 
                    created_date = datetime.now()
                )
                new_store.save()
                
                if platform == "Amazon":
                    client_id = request.POST.get("Client Id")
                    client_secret = request.POST.get("Client Secret")
                    refresh_token = request.POST.get("Refresh Token")
                    new_amazon_store = AmazonCredentials.objects.create(
                        storepforile = new_store, client_id = client_id,
                        client_secret = client_secret, refresh_token = refresh_token
                    )
                    new_amazon_store.save()
                elif platform == "Shopify":
                    pass
            return redirect('dashboard:home')
        return render(request,"add_store.html", context=context)
    except Exception as e:
        print(f"add_store error : \n{e}")