
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate

from .models import Customers

# Create your views here.
def index(request):
    return render(request, "index.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_page(request):
    if request.user.is_authenticated:
        return redirect(home_page)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
           if user.is_superuser:
                messages.info(request, "Not Valid user")
                return redirect("/login")
           else:
                login(request, user)
                return redirect("/home")

        else:
                messages.info(request, "Invalid Username and Password")
                return redirect("/login")

    else:
        return render(request, 'loginpage.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_page(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    return redirect(login_page)


def logout_page(request):
    if request.user.is_authenticated:
        request.session.flush()

    return redirect(login_page)
def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
    
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email id already taken")
                return redirect("register")
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name)
                user.save();
                messages.info(request,"User created")
                return redirect("login")

        else:
            messages.info(request,"Password Not matching")

        return redirect("register")

    else:
        return render(request, "register.html")

