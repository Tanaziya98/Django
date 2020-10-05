from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [
   path('',views.index,name="index"),
   path('handleblog',views.handleblog,name="handleblog"),
   path('services',views.services,name="services"),
   path('about',views.about,name="about"),
   path('contact',views.contact,name="contact"),
   path('signup',views.signup,name="signup"),
   path('login',views.handlelogin,name="handlelogin"),
   path('logout',views.handlelogout,name="handlelogout"),
   path('addpost',views.addpost,name="addpost"),
]
