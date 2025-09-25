from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View

from authorization.forms import LoginForm

# Create your views here.
        
def signin(request):
    form = None
    try:
        if request.method == "POST":
            form = LoginForm(request, data = request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                username = form.cleaned_data.get("username")
                password =  form.cleaned_data.get("password")
                
                authenticated_user = authenticate(
                    request, username = username, password = password
                )
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect('dashboard:home')
        else:
            form = LoginForm()
        return render(request,"auth/auth_form.html",{"form" : form})
    except Exception as e:
        return HttpResponse(e)
        
@login_required
def signout(request):
    try:
        logout(request)
        return redirect('dashboard:home') 
    except Exception as e:
        print(e)
    