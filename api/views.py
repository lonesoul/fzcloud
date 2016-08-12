# coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
import datetime,json,md5,sys,os,time,uuid
#from api.models import *
import threading
import random
import requests

# Create your views here.

def index(request):

    if request.method == 'POST':
        method = request.POST['method']
        if method:
            params = request.POST.get('params')
            params = json.loads(params)
            if method == 'GET':
                    return_data = {"code":10000,"msg":""}
                    if request.POST['action'] == 'userman':
                        from Xclass.UsermanClass import UsermanHandle
                        Data= {
                            "Uid":request.session.get('Uid')
                        }
                        return_data = UsermanHandle(params,Data).Person()                      
                    if request.POST['action'] == 'asset':
                        from Xclass.AssetClass import AssetHandle
                        Data= {
                            "Uid":request.session.get('Uid')
                        }
                        return_data = AssetHandle(params,Data).Person()                    
                    if request.POST['action'] == 'contact':
                        from Xclass.ContactClass import ContactHandle
                        Data= {
                            "Uid":request.session.get('Uid')
                        }
                        return_data = ContactHandle(params,Data).Person()
                    if request.POST['action'] == 'login':
                        from Xclass.XloginClass import LoginHandle
                        return_data = LoginHandle(params).login()
                        if return_data['code'] == 0:
                            request.session['UserName'] = params['user']
                            request.session['UserId'] = return_data['UserId']
                            request.session['Region'] = return_data['region']
                            del return_data['UserId']
                    elif request.POST['action'] == "region":
                        from Xclass.XregionClass import RegionHandle
                        user_info = {
                            "UserId" : request.session.get('UserId'),
                            "UserName" : request.session.get("UserName"),
                            "Region" : request.session.get('Region'),
                        }
                        if params['action'] == 'CreateRegion':
                            return_data = RegionHandle(params,user_info).create_region()
                    elif request.POST['action'] == 'keyproxy':
                        from Xclass.XkeyproxyClass import KeyproxyHandle
                        user_info = {
                            "UserId" : request.session.get('UserId'),
                            "UserName" : request.session.get("UserName"),
                            "Region" : request.session.get('Region'),
                        }
                        if params['action'] == 'CreateUser':
                            return_data = KeyproxyHandle(params,user_info).create_user()
                        if params['action'] == 'CreateService':
                            return_data = KeyproxyHandle(params,user_info).create_service()
                        if params['action'] == 'DescribeServiceList':
                            return_data = KeyproxyHandle(params,user_info).describe_serviceList()
                        if params['action'] == 'CreatePoint':
                            return_data = KeyproxyHandle(params,user_info).create_point()
                        if params['action'] == 'CreateImage':
                            #file = request.FILES['fileToUpload']
                            #fileValues = ''.join(file.chunks())
                            #params['fileValues'] = fileValues
                            return_data = KeyproxyHandle(params,user_info).image_handle()
                    return_data = json.dumps(return_data)
                    return HttpResponse(return_data)
            else:
                    return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')
