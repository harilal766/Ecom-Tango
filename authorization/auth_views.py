from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# Create your views here.
def login(request):
    return render(request,"auth.html")

def signup(request):
    try:
        if request.method == "POST":
            
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            new_user = User.objects.create_user(
                username=username, password=password
            )
            new_user.save()
            return redirect('dashboard:home')
            
        return render(request,"home.html")
    except Exception as e:
        print(e)
    