#!/usr/bin/env python
# encoding: utf-8


from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response
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

def index(request):
    indextitcon = "概览"
    
    #return render_to_response('index.html',{"indextitcon":indextitcon,"data_center":data_center})
    return render_to_response('index.html',locals())
    
    
    #http://inf.jcloud.com/css/jcloud_new/gz_images/stepArrow.jpg
