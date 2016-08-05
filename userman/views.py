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

def user(request):
    indextitcon = "用   户"
    type = "user"
    return render_to_response('user.html',locals())
    
    #return render_to_response('instance.html',locals(),context_instance=RequestContext(request))
    #return render_to_response('instance.html',{"indextitcon":indextitcon,"type":type,"data_center":data_center})

def usergroup(request):
    indextitcon = "用户组"
    type = "usergroup"
    return render_to_response('usergroup.html',locals())

def udetails(request,details):
    indextitcon = "用户详情"
    type = "user"
    print type
    print '----------------------------------'
    return render_to_response('udetails.html',locals())
    
