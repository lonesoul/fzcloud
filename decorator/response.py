#coding=utf8

"""
    Decorator response json_response and request type error
    author: shengyuan
    
    date: 2016-7-6

"""
import json
import logging
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

def set_log(level, filename='jumpserver.log'):
    """
    return a log file object
    根据提示设置log打印
    """
    log_file = os.path.join(LOG_DIR, filename)
    if not os.path.isfile(log_file):
        os.mknod(log_file)
        os.chmod(log_file, 0777)
    log_level_total = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARN, 'error': logging.ERROR,
                       'critical': logging.CRITICAL}
    logger_f = logging.getLogger('jumpserver')
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_total.get(level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    return logger_f
def post_only(f):

    """ Ensures a method is post only"""
    
    def wrapped_f(request):
        if request.method != "POST":
            response = HttpResponse(json.dumps({"error": "This method only accepts posts!"}))
            
            response.status_code = 500
            
            return response
            
    return wrapped_f
    
def json_response(f):
    """
        Return the response as json, and return a 500 error code if an error exits 
    """
    
    def wrapped(*args, **kwargs):
        result = f(*args, **kwargs)
        
        response = HttpResponse(json.dumps(result))
        
        if type(result) == dict and "error" in result:
            response.status_code = 500
            
            
        return response
def validate_login_status(func):

    """ Ensures a method is post only"""
    def wrapped_f(request, *args, **kwargs):
        if request.session.get("Uid") is None:
            return HttpResponseRedirect('/')
        return func(request,*args, **kwargs)
    return wrapped_f

