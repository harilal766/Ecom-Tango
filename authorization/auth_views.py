from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login


# Create your views here.
def login(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            authenticated_user = authenticate(
                request, username = username, password = password
            )
            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                return redirect('dashboard:home')            
        return render(request,"home.html")
    except Exception as e:
        print(e)
    