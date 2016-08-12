#!/usr/bin/env python
# encoding: utf-8

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from api.models import c_group,assets,agroups
import md5
import datetime
import StringIO
#from validate import create_validate_code
#from sendvaliemail import sendmail
import random
import os
import time
import shutil
from decorator.response import validate_login_status


@validate_login_status
def asset(request):
    indextitcon = "资产"
    type = "asset"
    UserName = request.session.get("UserName")
    asset_l = []
    asset_list = assets.objects.filter(Uid=request.session.get("Uid")).order_by("CreateTime")
    for asset_d in asset_list:
        if asset_d.GroupId:
            agroup_d = agroups.objects.filter(uuid=asset_d.GroupId).first()
            asset_d.GroupName = agroup_d.Name
        asset_l.append(asset_d)
    asset_list = asset_l
    return render_to_response('asset.html',locals())
    
    #return render_to_response('instance.html',locals(),context_instance=RequestContext(request))
    #return render_to_response('instance.html',{"indextitcon":indextitcon,"type":type,"data_center":data_center})
@validate_login_status
def assetgroup(request):
    indextitcon = "资产组"
    type = "assetgroup"
    UserName = request.session.get("UserName")
    agroups_list = agroups.objects.filter(Uid=request.session.get("Uid")).order_by("CreateTime")
    return render_to_response('assetgroup.html',locals())
@validate_login_status
def agdetails(request,details):
    #查询当前联系人id 信息
    a_g_details = agroups.objects.filter(uuid=request.GET.get("agroupsId")).first()
    indextitcon = "资产组详情"
    type = "assetgroup"
    UserName = request.session.get("UserName")
    
    a_g_list = assets.objects.filter(GroupId=a_g_details.uuid)
    clist = []
    for asset_details in a_g_list:
        cdict = {
            "uuid" : asset_details.uuid,
            "HostName" : asset_details.HostName,
            "HostIp" : asset_details.HostIp,
            "System" : "%s %s" % (asset_details.SystemType,asset_details.SystemVersion),
            "CreateTime" : asset_details.CreateTime
        }
        clist.append(cdict)
    return render_to_response('agdetails.html',locals())
    
