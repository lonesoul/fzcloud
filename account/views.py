#!/usr/bin/env python
# encoding: utf-8


from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response
from django.db.models import Count
#from django.template import RequestContext
from api.models import users
#import md5
#import datetime
#import StringIO
#from validate import create_validate_code
#from sendvaliemail import sendmail
#import random
#import os
#import time
#import shutil
#import json
from decorator.response import *

from api.Xclass.PyCryptClass import * 
from django.views.decorators.csrf import csrf_exempt
    
        
        

#@post_only
@csrf_exempt
def login(request):
    """
        登录页面
    """
    error = ''
    if request.method == "GET":
        return render_to_response('login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = users.objects.filter(UserName=username,Password=PyCrypt.md5_crypt(password))
            if user.count():
                user_details = user.first()
                if user_details.Status:
                    request.session['Uid'] = user_details.uuid
                    request.session['UserName'] = user_details.UserName
                    request.session['Name'] = user_details.Name
                    request.session['Groups'] = user_details.Groups
                    request.session['Power'] = user_details.Power
                    return HttpResponseRedirect('/index/')
                else:
                    error = "用户未激活"
                
            else:
                error = "用户名或密码错误"
            
        else:
            error = "用户名或密码错误"
    return render_to_response('login.html', {'error': error})
   
'''   
@post_only
def register(request):


    result = None
    
    try:
        user = Users.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        
        for field in ['first_name', 'last_name']:
            if field in request.POST:
                setattr(user,field, request.POST['field'])
        user.save()
        return {"success": True}
    except KeyError as e:
        return {"error": str(e)}
    
    
    return response
'''

def logout(request):
    try:
        if request.session.get("Uid"):pass
        del request.session['Uid']
    except:
        pass
    
    return HttpResponseRedirect('/')