#!/usr/bin/env python
# *-* coding: utf-8 *-*
#Author: Yuan Sheng
import uuid

from api.models import region
from api.lib import XcloudLib

class KeyproxyHandle(object):

    """
    """
    def __init__(self,parame,user_info):
        self.parame = parame
        self.user_info = user_info
        self.return_data = {}
    #获取当前区域信息
    def _region_info(self):
        region_details = region.objects.filter(RegionId=self.user_info['Region']).first()
        if region_details:
            return_data = {
                "code":0,
                "info":region_details,
            }
        else:
            return_data = {
                "code":1,
            }
        return return_data
        
    def image_handle(self):
        print self.user_info
        region_details = self._region_info()
        if region_details['code'] == 0:
            parame={
                "Token" : region_details['info'].Token,
                "service" : "images",
                "parame" : self.parame,
                "UserId" : self.user_info['UserId'],
            }
            resulte = XcloudLib.http_request(parame,region_details['info'].RegionAddress)
            print resulte
            if resulte['code'] == 0:
                return_data['code'] = 0
                return_data['msg'] = ""
                
            else:
                self.return_data['code'] = 10000
                self.return_data['msg'] = "对不起，无法为您创建镜像."
                if resulte['code'] == 1003:
                    self.return_data['msg'] = "对不起，您提交的所在代理服务器上镜像位置不存在."
        else:
            print 'a11111111111111111'
            self.return_data['code'] = 10000
            self.return_data['msg'] = "对不起，提交信息有误."
        return self.return_data
    def create_user(self):
        return_data = {}
        #查询区域ID是否存在 如果存在则返回创建失败 不存在则插入
        #获取当前区域的point
        region_details = self._region_info()
        if region_details['code'] == 0:
            self.parame['password'] = XcloudLib.md5Encrypt(self.parame['password'])
            parame={
                "Token" : region_details['info'].Token,
                "service" : "keyproxy",
                "parame" : self.parame
            }
            resulte = XcloudLib.http_request(parame,region_details['info'].RegionAddress)
            if resulte['code'] == 0:
                return_data['code'] = 0
                return_data['msg'] = ""
            else:
                return_data['code'] = 10000
                return_data['msg'] = "对不起，提交信息有误."
        else:
            return_data['code'] = 10000
            return_data['msg'] = "对不起，提交信息有误."
        return return_data
    def create_service(self):
        return_data = {}
        region_details = self._region_info()
        if region_details['code'] == 0:
            parame={
                "Token" : region_details['info'].Token,
                "service" : "keyproxy",
                "parame" : self.parame
            }
            resulte = XcloudLib.http_request(parame,region_details['info'].RegionAddress)
            if resulte['code'] == 0:
                return_data['code'] = 0
                return_data['msg'] = ""
            else:
                return_data['code'] = 10000
                return_data['msg'] = "对不起，提交信息有误."
        else:
            return_data['code'] = 10000
            return_data['msg'] = "对不起，提交信息有误."
        return return_data
    def describe_serviceList(self):
        return_data = {}
        region_details = self._region_info()
        if region_details['code'] == 0:
            parame={
                "Token" : region_details['info'].Token,
                "service" : "keyproxy",
                "parame" : self.parame
            }
            resulte = XcloudLib.http_request(parame,region_details['info'].RegionAddress)
            if resulte['code'] == 0:
                return_data['code'] = 0
                return_data['msg'] = resulte['msg']
            else:
                return_data['code'] = 10000
                return_data['msg'] = "对不起，提交信息有误."
        else:
            return_data['code'] = 10000
            return_data['msg'] = "对不起，提交信息有误."
        return return_data
    def create_point(self):
        return_data = {}
        region_details = self._region_info()
        if region_details['code'] == 0:
            parame={
                "Token" : region_details['info'].Token,
                "service" : "keyproxy",
                "parame" : self.parame
            }
            resulte = XcloudLib.http_request(parame,region_details['info'].RegionAddress)
            if resulte['code'] == 0:
                return_data['code'] = 0
                return_data['msg'] = resulte['msg']
            else:
                return_data['code'] = 10000
                return_data['msg'] = "对不起，提交信息有误."
        else:
            return_data['code'] = 10000
            return_data['msg'] = "对不起，提交信息有误."
        return return_data
