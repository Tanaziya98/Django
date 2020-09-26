from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')

def handleblog(request):
    if  not request.user.is_authenticated:
        messages.error(request,"Please Login  & Try Again")
        return redirect('/login')
        
    return render(request,'handleblog.html')    

def services(request):
    return render(request,'services.html')    

def about(request):
    return render(request,'about.html')    

def contact(request):
    return render(request,'contact.html')    

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1!=pass2:
            messages.warning(request,"password not matched")

        try:
            if User.objects.get(username=username):
                return HttpResponse("Username Already been Taken")    
        except Exception as identifier:
            pass     
        try:
            if User.objects.get(email=email):
                return HttpResponse("Email already exist")    
        except Exception as identifier:
            pass        
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=firstname
        myuser.last_name=lastname
        myuser.save()
        return HttpResponse("Sign Up Successfull")    


    return render(request,'auth/signup.html')    

def handlelogin(request):
    if request.method=="POST":
        handleusername=request.POST.get('username')
        handlepassword=request.POST.get('pass1')
        user=authenticate(username=handleusername,password=handlepassword)
        if user is not None:
            login(request,user)
            messages.info(request,"Welcome To My Website")
            return redirect('/')
        else:
            messages.warning(request,"Invalid Credentials")  
            return redirect('/login')
    return render(request,'auth/login.html')


def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/login')
