#!/usr/bin/env python
# *-* coding: utf-8 *-*

from api.models import users
from api.lib import XcloudLib

class LoginHandle(object):

    """
    """
    def __init__(self,parame):
        self.parame = parame

    def login(self):
        return_data = {}
        user_v = users.objects.filter(UserName=self.parame['user']).filter(Password=XcloudLib.md5Encrypt(self.parame['pass'])).first()
        if user_v:
            print 
            return_data['code'] = 0
            return_data['msg'] = ''
            return_data['region'] = user_v.Region
            return_data['UserId'] = user_v.id
        else:
            return_data['code'] = 10000
            return_data['msg'] = "您输入的用户名或密码错误."
        return return_data
