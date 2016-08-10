#!/usr/bin/env python
# *-* coding: utf-8 *-*

import uuid

from api.models import region
from api.lib import XcloudLib

class RegionHandle(object):

    """
    """
    def __init__(self,parame,user_info):
        self.parame = parame
        self.user_info = user_info
    def create_region(self):
        return_data = {}
        #查询区域ID是否存在 如果存在则返回创建失败 不存在则插入
        region_v = region.objects.filter(RegionId=self.parame['regionid']).first()
        if not region_v:
            #插入数据

            region(RegionName=self.parame['regionname'],RegionId=self.parame['regionid'],\
                        Status=0,RegionAddress=self.parame['regionadd'],\
                        Token=XcloudLib.md5Encrypt(str(uuid.uuid1()))).save()
            return_data['code'] = 0
            return_data['msg'] = ''
        else:
            return_data['code'] = 10000
            return_data['msg'] = "您输入的用户名或密码错误."
        return return_data
