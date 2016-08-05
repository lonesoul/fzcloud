#!/usr/bin/env python
# encoding: utf-8


from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
#from api.models import *
import md5
import datetime
import StringIO
#from validate import create_validate_code
#from sendvaliemail import sendmail
import random
import os
import time
import shutil

def webservice(request):
    indextitcon = "WEB 服务"
    type = "webservice"
    return render_to_response('webservice.html',locals())
    #return render_to_response('instance.html',locals(),context_instance=RequestContext(request))
    #return render_to_response('instance.html',{"indextitcon":indextitcon,"type":type,"data_center":data_center})

def database(request):
    indextitcon = "数据库"
    type = "database"
    return render_to_response('database.html',locals())

def caches(request):
    indextitcon = "缓存"
    type = "caches"
    return render_to_response('caches.html',locals())
def nosql(request):
    indextitcon = "NoSQL"
    type = "nosql"
    return render_to_response('nosql.html',locals())
def information(request):
    indextitcon = "消息队列"
    type = "information"
    return render_to_response('information.html',locals())
def lbs(request):
    indextitcon = "负载均衡"
    type = "lbs"
    return render_to_response('lbs.html',locals())    
def details(request,zone,details):
    indextitcon = "新建云主机"
    data_center = zone
    type = "instance"
    return render_to_response('instance%s.html'%details,{"indextitcon":indextitcon,"type":type,"data_center":data_center})
    
