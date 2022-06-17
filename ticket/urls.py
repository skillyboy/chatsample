from django.urls import path
from . import views
# from rest_framework import routers

# from .api import ChatViewSet
from django.urls import path, include
from .views import *
from django.views.generic.base import TemplateView
# from .views import group_message_list
from django.urls import re_path as url

# from chatapp import views


# router = routers.DefaultRouter()
# router.register("profile", ProfileViewSet)
urlpatterns = [
    
    path('', views.index, name='index'),
    path('video', views.video, name='video'),
    
    path('signup/', views.signupform, name='signupform'),
    path('login/', views.loginfunc, name='login'),
    path('logout/', views.logoutfunc, name='logout'),
    path('password', views.password, name='password'),
    

]

