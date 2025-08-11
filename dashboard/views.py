from django.shortcuts import render, redirect
from amazon.models import *
from shopify.models import *

# Create your views here.
def home(request):
    return render(request,'dashboard.html')

def add_store(request):
    context = {
        "platforms" : ("Amazon", "Shopify")
    }
    try:
        if request.method == "POST":
            platform = request.POST.get("platform")
            if platform == "Amazon":
                pass
            elif platform == "Shopify":
                pass
            
            storename = request.POST.get("Name of the store")
            print(storename, platform)
            
            redirect('dashboard:home')
    except Exception as e:
        print(e)
    return render(request,"add_store.html", context=context)