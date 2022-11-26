from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.cache import cache_control




# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):

    if request.user.is_authenticated:
        return redirect(adminhome)
    
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            print("done")
            if user.is_superuser:
                print("superuser")
                auth.login(request, user)
                return redirect("adminhome")
            else:
                messages.info(request, "Only admin can login")
                return render(request,"admin.html")

        else:
            messages.info(request, "Invalid Username and Password")
            return render(request,"admin.html")

    else:
        return render(request,'admin.html')



        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminhome(request):
    if request.user.is_authenticated:

        context={'localusers':User.objects.all()}

        return render(request, "adminhome.html",context)
    
    return redirect(adminlogin)

def adminlogout(request):
    if request.user.is_authenticated:
        request.session.flush()

    return redirect(adminlogin)

def delete(request,id):

    user=User.objects.get(id=id)
    user.delete()
    return redirect(adminhome)

def update(request,id):
    if request.method=='POST':
        name=request.POST['firstname']
        username=request.POST['username']
        email=request.POST['email']

        updateuser=User.objects.get(id=id)
        updateuser.first_name=name
        updateuser.username=username
        updateuser.email=email
        updateuser.save()
        return redirect(adminhome)
    else:
        user=User.objects.get(id=id)
        context={'localuser':user}
        return render(request,"adminupdate.html",context)

def add(request):
    if request.method=='POST':
        name=request.POST['firstname']
        username=request.POST['username']
        email=request.POST['email']

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect("add")
        elif User.objects.filter(email=email).exists():
            messages.info(request,"Email id already taken")
            return redirect("add")
        elif User.objects.filter(first_name=name).exists():
            messages.info(request,"Name is already taken")
            return redirect("add")
        else:
            adduser=User(first_name=name,username=username,email=email)
            adduser.save()
            return redirect("adminhome")

        
        
    else:
        
        return render(request,"adminadd.html")

def search(request):
    
        usrname=request.GET['username']
        print(usrname)
        searchuser = User.objects.filter(username__contains=usrname)
        
        
        return render(request,"adminsearch.html",{'usr':searchuser})
        
       

    
