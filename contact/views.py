#!/usr/bin/env python
# encoding: utf-8

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from api.models import contacts,cgroups,c_group
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
def contact(request):
    indextitcon = "联系人"
    type = "contact"
    UserName = request.session.get("UserName")
    contact_list = contacts.objects.filter(Uid=request.session.get("Uid")).order_by("CreateTime")
    return render_to_response('contact.html',locals())
    
    #return render_to_response('instance.html',locals(),context_instance=RequestContext(request))
    #return render_to_response('instance.html',{"indextitcon":indextitcon,"type":type,"data_center":data_center})
@validate_login_status
def contactgroup(request):
    indextitcon = "联系组"
    type = "contactgroup"
    UserName = request.session.get("UserName")
    cgroups_list = cgroups.objects.filter(Uid=request.session.get("Uid")).order_by("CreateTime")
    return render_to_response('contactgroup.html',locals())

def cgdetails(request,details):
    #查询当前联系人id 信息
    c_g_details = cgroups.objects.filter(uuid=request.GET.get("cgroupsId")).first()
    indextitcon = "联系组详情"
    type = "contactgroup"
    UserName = request.session.get("UserName")

    c_g_list = c_group.objects.filter(C_Groupid=c_g_details.uuid)
    clist = []
    for cg_details in c_g_list:
        print cg_details.Contactid
        c_details = contacts.objects.filter(uuid=cg_details.Contactid).first()
        cdict = {
            "uuid" : c_details.uuid,
            "Name" : c_details.Name,
            "Phone" : c_details.Phone,
            "Email" : c_details.Email,
            "CreateTime" : c_details.CreateTime
        }
        clist.append(cdict)
    print clist
    return render_to_response('cgdetails.html',locals())
    
