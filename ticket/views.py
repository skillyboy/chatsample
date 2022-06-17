
from django.core.mail import send_mail
from django.db.models.query_utils import subclasses
from django.http import HttpResponse
from . forms import SignupForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import datetime
from django.core import serializers
# from rest_framework import viewsets
# from .serializers import ProfileSerializer, MessageSerializer, GroupSerializer, LiveMessageSerializer, ChatSerializer

from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponse, request

import pdb
from django.contrib import messages
import json
# from campaigns.models import CreateCamp
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError  # add this to your imports
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

import re
import json
import socket
import subprocess
from django.utils.crypto import get_random_string
import os





# @login_required(login_url='/login')
def video(request):
    return render(request, 'video.html')




# @login_required(login_url='/login')
# def index(request):
#     if not request.user.is_authenticated:
#         print('index ********** session :', request.session['company'])
#         company = request.session['company']
#         return render(request, "index.html", {'co': company, 'ho': 'snaskjjsk'})
#     else:
#         username = request.user.username
#         # id = getUserId(request.user.username)
#         user = User.objects.get(id=request.user.id)
#         profile = Profile.objects.get(user=request.user)
#         profiles = Profile.objects.filter(
#             company=profile.company).exclude(user=request.user)
#         connection = Connection.objects.all()
#         # groups=GroupMember.objects.all()
#         friends = (Friends.objects.filter(user1=request.user) |
#                    Friends.objects.filter(user2=request.user))
#         com_id = Company.objects.get(company_uuid=request.session['company'])
#         groups = list()
#         for c in connection:
#             if c.user == request.user and c.company.company_uuid == request.session['company']:
#                 groups.append(Group.objects.get(id=c.group.id))
#         # groups = groups.filter(title=Company.objects.get(company_uuid=request.session['company']).company)
#         # chat_list = get_chat_list(request, id, friends, groups)
#         # pdb.set_trace()
#         temp = Profile.objects.get(user_id=request.user.id)
#         company = temp.company
#         company_id = request.session['company']
#         # Camp = CreateCamp.objects.all()
#         l=[]
#         for x in profiles:
#            l.append(x.user) 
#         # for f in chat_list:
#         #     print("BUUUUUUGGGGGEEEEERRRRRR")
#         #     if f.chat_type == "direct":
                
#         #         pdb.set_trace()
#         #         f.pics = Profile.objects.get(id=f.id)
#         #         print(f.pics.user_files)
#         return render(
#             request,
#             "chat-home.html",
#             {
#                 "friends": friends,
#                 "groups": groups,
#                 "user": l,
#                 "company": company,
#                 "company_id": company_id,
#                 # "chat_list": chat_list,
#                 # "camp": Camp,
#                 'users': profiles
#             },
#         )





def index(request):
    return render(request, 'index.html')

def signupform(request):
    reg = SignupForm()
    if request.method == 'POST':
        reg = SignupForm(request.POST)
        if reg.is_valid():
            new = reg.save()
            login(request, new)
            messages.success(request, 'Signup successfull!')
            return redirect('index')
        else:
            messages.warning(request, reg.errors)
            return redirect('signupform')

    context = {
        'reg': reg
    }

    return render (request,'signup.html', context)

def logoutfunc(request):
    logout(request)
    return redirect('index')

def loginfunc(request):  
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, 'successful')
            return redirect('index')
        else:
            messages.info(request, 'username/password incorrect')
            return redirect('login')
    return render (request, 'login.html')

def password(request):
    update = PasswordChangeForm(request.user)
    if request.method == 'POST':
        update = PasswordChangeForm(request.user, request.POST)
        if update.is_valid():
            user=update.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password update successful!')
            return redirect('index')
        else:
            messages.error(request, update.errors)
            return redirect('password')

    context = {
        'update': update
    }

    return render(request, 'password.html', context)





def send(request):  
    if request.method=="POST":
        message_name= request.POST['name']
        message = request.POST['message']
        message_email= request.POST['email']
        # send an email
        send_mail(
            message_name,
            message,
            message_email,
            ['skillytechy@gmail.com'],
        )
        return render(request, 'event.html', {'message_name': message_name})
    else:
        return render(request, 'event.html', {})
   