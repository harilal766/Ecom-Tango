from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View

from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
class AuthView(View):
    def get(self,request):
        form = None
        try:
            form = AuthenticationForm()
            return render(request,"auth/auth_form.html",{"form":form})
        except Exception as e:
            return HttpResponse(e)
        
@login_required
def signout(request):
    try:
        logout(request)
        return redirect('dashboard:home') 
    except Exception as e:
        print(e)
    