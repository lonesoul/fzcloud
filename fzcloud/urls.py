"""fzcloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    #url(r'^([^/]+)/index/$','index.views.index'),
    url(r'^index/','index.views.index'),
    url(r'^webservice/$','microservice.views.webservice'),
    url(r'^database/$','microservice.views.database'),
    url(r'^caches/$','microservice.views.caches'),
    url(r'^nosql/$','microservice.views.nosql'),
    url(r'^information/$','microservice.views.information'),
    url(r'^lbs/$','microservice.views.lbs'),
    
    url(r'^asset/$','asset.views.asset'),
    url(r'^assetgroup/$','asset.views.assetgroup'),
    
    url(r'^user/$','userman.views.user'),
    url(r'^user/([^/]+)$','userman.views.udetails'),    
    url(r'^usergroup/$','userman.views.usergroup'),
    url(r'^contact/$','contact.views.contact'),
    url(r'^contactgroup/$','contact.views.contactgroup'),
    url(r'^contactgroup/([^/]+)$','contact.views.cgdetails'),   

]

