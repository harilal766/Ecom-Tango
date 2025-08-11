from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'dashboard.html')

def add_store(request):
    context = {
        "platforms" : ("Amazon", "Shopify")
    }
    return render(request,"add_store.html", context=context)