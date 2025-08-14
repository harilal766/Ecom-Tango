from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dashboard.d_views import view_store

# Create your views here.
def signin(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            authenticated_user = authenticate(
                request, username = username, password = password
            )
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('dashboard:home')     
        return render(request,"home.html")
    except Exception as e:
        return render(request,"error.html",{"error" : e})
        
@login_required
def signout(request):
    try:
        logout(request)
        return redirect('dashboard:home') 
    except Exception as e:
        print(e)
    