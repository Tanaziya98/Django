from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Contact,BlogPosts
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage


# Create your views here.
def index(request):
    return render(request,'index.html')

def handleblog(request):
    if  not request.user.is_authenticated:
        messages.error(request,"Please Login  & Try Again")
        return redirect('/login')
    posts=BlogPosts.objects.all()
    context={'posts': posts}   
    return render(request,'handleblog.html',context)    

def services(request):
    return render(request,'services.html')    

def about(request):
    return render(request,'about.html')    

def contact(request):
    if request.method=="POST":
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        phone=request.POST.get('num')
        description=request.POST.get('desc')
        contact_query=Contact(name=fullname,email=email,number=phone,description=description)#left hand attribute should be same as given in models.py i.e the table
        contact_query.save()
        #email starts here
        from_email=settings.EMAIL_HOST_USER
        # email starts here
        # your mail starts here
        connection=mail.get_connection()
        email_mesge=mail.EmailMessage(f'Website Email from {fullname}',f'Email from : {email}\nUser Query :{description}\nPhone No : {phone}',from_email,['tanaziyamb@gmail.com'],connection=connection)
        email_user=mail.EmailMessage('AIROBOTICA',f'Hello{fullname}\n Thanks for Contacting Us We will Resolve Your Problem Soon\n Thank you\n',from_email,[email],connection=connection)
        connection.send_messages([email_mesge,email_user])
        connection.close()
        messages.info(request,"Thanks for Contacting Us")
        return redirect('/contact')
    

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

def addpost(request):
    if request.method=="POST":
        title=request.POST.get('title')
        content=request.POST.get('desc')
        name=request.POST.get('name')
        files=request.FILES['file']
        query=BlogPosts(title=title,content=content,author=name,img=files)
        query.save()
        messages.info(request,"Your Post Has Been Added")
        return redirect('/handleblog')
    
    return render(request,'addpost.html')    

def search(request):
    query=request.GET['search']
    if len(query)>75:
        allPosts=BlogPosts.objects.none()
    else:
        allPostsTitle=BlogPosts.objects.filter(title__icontains=query)
        allPostsContent=BlogPosts.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent)   
    if allPosts.count()==0:#if no query matchs
        messages.warning(request,"No Search Results")

    params={'allPosts':allPosts,'query':query}         
    
    return render(request,'search.html',params)    
