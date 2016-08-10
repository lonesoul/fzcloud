# -*- coding: utf-8 -*-

#导出常用模块
import datetime
import json
import md5
import sys
import os
import uuid

#导出数据结构模块
from api.models import *
from NcloudHostClass import HandleHost
#操作cache类
def Create_Redis(Data,params):

    return_data = {
        "code" : 10101,
        "msg" : "action completed fails",
    }
    # 根据类型判断
    HostType = "cache"
    if params['CacheMode'] == "1":
        image_id_M = 'centos66x64a' #redis
        image_id_S = 'centos66x64a-xx'
    elif params['CacheMode'] == "0":
        image_id_M = 'centos66x64a' #redis cluster
    else:
        image_id_M = 'centos66x64a' #memcached

    parame = dict(
        image_id = image_id_M,
        cpu = 1,
        memory = int(params['CacheSize'])*1024,
        HostType = HostType,
        vswid = params['cacheswitch'],
    )
    #根据节点数判断 如果节点数大于1 则 创建一个 master 节点 否则创建多个节点
    
    if int(params['CacheNum']) >1:
        for  i in xrange(int(params['CacheNum'])):
            if i == 0:
                #Handle_Result = HandleHost(Data,parame).CreateEch()
                print parame 
            else:
                parame['image_id'] = image_id_S
                print parame
                #Handle_Result = HandleHost(Data,parame).CreateEch()
    else:
        Handle_Result = HandleHost(Data,parame).CreateEch()
        if Handle_Result['code'] == 0:
            #取HostInfo 创建 CacheInfo  CacheNodeInfo
            CacheUUID = str(uuid.uuid1())
            CacheId = 'c-%s' % CacheUUID[:8]
            CacheInfo(
                            CacheId = CacheId,
                            CacheName = params['CacheName'],
                            Bewrite = '',
                            Label = '',
                            MaxAvaMem = parame['memory'],
                            Port = 6379,
                            Status = 1,
                            Version = 'Redis2.8.17',
                            VersionType = 1,
                            Zone = Data['Zone'],
                            NodeNum = int(params['CacheNum']),
                            Mem = parame['memory'],
                            Type = 1,
                            CcfgId = params['cachecfg'],
                            Network = params['cacheswitch'],
                            CacheUUID = CacheUUID,
                            UserId = Data['UserId'],
            ).save()
            CacheNodeInfo(
                                    NodeId = Handle_Result['HostInfo']['HostId'],
                                    NodeName = Handle_Result['HostInfo']['HostName'],
                                    Status = 0,
                                    NodeIp = Handle_Result['HostInfo']['HostIp'],
                                    Category = 'redis',
                                    NodeType = 0,
                                    Network = params['cacheswitch'],
                                    AlarmStatus = 1,
                                    Zone = Data['Zone'],
                                    Cpu = parame['cpu'],
                                    Mem = parame['memory'],
                                    ImagesId = image_id_M,
                                    VncIp = Handle_Result['HostInfo']['KVMIp'],
                                    VncPort = Handle_Result['HostInfo']['VNCPort'],
                                    Macs = Handle_Result['HostInfo']['HostMac'],
                                    TapUUID = Handle_Result['HostInfo']['TapUUID'],
                                    TenantId = Handle_Result['HostInfo']['TenantId'],
                                    VlandId =Handle_Result['HostInfo']['VlanId'],
                                    UserId = Data['UserId'],
                                    CacheUUID = CacheUUID,
                                    NodeUUID = Handle_Result['HostInfo']['HostUUID'],
                                    RecordTime = datetime.datetime.now(),
            ).save()
            return_data = {
                "code" : 0,
                "msg" :Handle_Result['msg'],
                "Status" : Handle_Result['Status'],
            }
        else:
            pass
    
    return return_data
