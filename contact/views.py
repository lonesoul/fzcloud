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

def contact(request):
    indextitcon = "联系人"
    type = "contact"
    return render_to_response('contact.html',locals())
    
    #return render_to_response('instance.html',locals(),context_instance=RequestContext(request))
    #return render_to_response('instance.html',{"indextitcon":indextitcon,"type":type,"data_center":data_center})

def contactgroup(request):
    indextitcon = "联系组"
    type = "contactgroup"
    print 
    return render_to_response('contactgroup.html',locals())

def cgdetails(request,details):
    indextitcon = "联系组详情"
    type = "contactgroup"
    print type
    print '----------------------------------'
    return render_to_response('cgdetails.html',locals())
    
