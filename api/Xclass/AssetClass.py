#!/usr/bin/env python
# *-* coding: utf-8 *-*

import datetime

from api.models import assets,agroups
from api.lib import XcloudLib
from uuid import uuid1
class AssetHandle(object):

    """
    """
    def __init__(self,parame,Data):
        self.parame = parame
        self.Data = Data
        self.return_data = {}
    def Person(self):
        if self.parame['action'] == 'addPerson':
            self._addPerson()
        elif self.parame['action'] == 'updatePerson':
            self._updatePerson()
        elif self.parame['action'] == 'deletePerson':
            self._deletePerson()
        elif self.parame['action'] == 'addAsset':
            self._addAsset()
        elif self.parame['action'] == 'newGroup':
            self._newGroup()
        elif self.parame['action'] == 'addDetailPerson':
            self._addDetailPerson()
        elif self.parame['action'] == 'addAssetToGroup':
            self._addAssetToGroup()
        elif self.parame['action'] == 'deleteAssetToGroup':
            self._deleteAssetToGroup()
        elif self.parame['action'] == 'deleteAGroup':
            self._deleteAGroup()
        return self.return_data
    def _deleteAGroup(self):
    
        agroups_n = agroups.objects.filter(uuid=self.parame["gid"])
        if agroups_n:
            assets.objects.filter(GroupId=self.parame["gid"]).update(GroupId="")
            agroups_n.delete()
            self.return_data['code'] = 0
        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "对不起，您提交的信息错误."      
        return self.return_data
    def _deleteAssetToGroup(self):
        #contact_u = contacts.objects.filter(Uid=self.Data['Uid']).filter(uuid=self.parame["cid"]).first()
        asset_u = assets.objects.filter(GroupId=self.parame["agroupsId"]).filter(Uid=self.Data['Uid']).first()
        if asset_u:
            #print contact_u.uuid
            asset_u.GroupId = ""
            asset_u.save()
            agroups_n = agroups.objects.filter(uuid=self.parame["agroupsId"]
                                               ).first()
            agroups_n.AssetNum = agroups_n.AssetNum -1
            agroups_n.save()
            self.return_data['code'] = 0
        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "对不起，您提交的信息错误."      
        return self.return_data
    def _addAssetToGroup(self):
        #严重联系组id是否存在存在则插入联系人关系表
        asset_g = agroups.objects.filter(Uid=self.Data['Uid']
                                           ).filter(uuid=self.parame['agroupsId']
                                           ).first()
        if asset_g:
            '''
            print self.parame['name']
            print self.parame['phone']
            print datetime.datetime.now()
            '''
            
            for aid in self.parame["alist"]:
                asset_d = assets.objects.filter(uuid=aid).first()
                asset_d.GroupId = self.parame['agroupsId']
                asset_d.save()
            asset_g.AssetNum = asset_g.AssetNum + len(self.parame["alist"])
            asset_g.save()
            self.return_data['code'] = 0
            self.return_data['msg'] = "添加联系人成功."   

        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "对不起，您提交的信息错误."
        return self.return_data      
    def _addDetailPerson(self):
        asset_u = assets.objects.filter(Uid=self.Data['Uid']).filter(GroupId='')

        data = []
        for asset_details in asset_u:
            if asset_details.uuid in self.parame['alist']:pass
            else:
                asset_d = {}
                asset_d["aid"] = asset_details.uuid
                asset_d["hostname"] = asset_details.HostName
                asset_d["hostip"] = asset_details.HostIp
                asset_d["system"] = "%s %s" % (asset_details.SystemType,asset_details.SystemVersion)
                data.append(asset_d)
        self.return_data['data'] = data
        self.return_data["code"] = 0
        
        return self.return_data
    def _newGroup(self):
        asset_g = agroups.objects.filter(Name=self.parame['grourName'])
        if asset_g:
            self.return_data['code'] = 10000
            self.return_data['msg'] = "您输入的联系组已经存在."
        else:
            a_g = agroups(uuid=uuid1(),
                          Name=self.parame['grourName'],
                          AssetNum=len(self.parame['clist']),
                          Uid=self.Data['Uid'])
            a_g.save()
            for cid in self.parame["clist"]:
                #查询asset 根据uuid查询结果 更新groupid
                asset_d = assets.objects.filter(Uid=self.Data['Uid']
                                                ).filter(uuid=cid).first()
                asset_d.GroupId = a_g.uuid
                asset_d.save()
            self.return_data['code'] = 0
            self.return_data['msg'] = "添加联系人成功."       
        return self.return_data        
    
    
    def _addAsset(self):
        asset_u = assets.objects.filter(Uid=self.Data['Uid']).filter(GroupId='')

        data = []
        for asset_details in asset_u:
            if asset_details.uuid in self.parame['alist']:pass
            else:
                asset_d = {}
                asset_d["aid"] = asset_details.uuid
                asset_d["hostname"] = asset_details.HostName
                asset_d["hostip"] = asset_details.HostIp
                asset_d["system"] = "%s %s" % (asset_details.SystemType,asset_details.SystemVersion)
                data.append(asset_d)
        self.return_data['data'] = data
        self.return_data["code"] = 0
        
        return self.return_data
    
    def _addPerson(self):
        assets_u = assets.objects.filter(HostName=self.parame['hostname'],
                                            HostIp=self.parame['hostip']
                                            ).first()
        if assets_u:
            self.return_data['code'] = 10000
            self.return_data['msg'] = "您输入的联系人信息已经存在."
        else:
            print self.parame
            #{u'status': u'1', u'manageuser': 0, u'hostname': u'o2o.10.3.6.27', u'hostip': u'10.3.6.27', u'action': u'addPerson', u'port': u'1022'}
            assets(uuid=uuid1(),
                   HostName = self.parame['hostname'],
                   HostIp = self.parame['hostip'],
                   OtherIp = "",
                   MAC = "",
                   ManageAccount = self.parame['manageuser'],
                   Port = int(self.parame['port']),
                   GroupId = '',
                   CPU = 0,
                   MEM = 0,
                   Disk = 0,
                   SystemType = '',
                   SystemVersion = '',
                   HostType = '',
                   OperatEnv = '',
                   HostStatus = '',
                   Status = int(self.parame['status']),
                   Uid = self.Data["Uid"],
                   ).save()
            '''
            print self.parame['name']
            print self.parame['phone']
            print datetime.datetime.now()
            
            contacts(uuid=uuid1(),
                     Name=self.parame['name'],
                     Email=self.parame['email'],
                     Phone=self.parame['phone'],
                     Uid=self.Data['Uid']).save()
            '''
            self.return_data['code'] = 0
            self.return_data['msg'] = "添加联系人成功."       
        return self.return_data
        
    def _updatePerson(self):
        
        assets_d = assets.objects.filter(Uid=self.Data['Uid']
                                            ).filter(uuid=self.parame["nowId"]
                                            ).first()
        if assets_d:
            assets_d.HostName = self.parame['hostname']
            assets_d.HostIp = self.parame['hostip']
            assets_d.OtherIp = self.parame['hostip']
            assets_d.MAC = self.parame['hostip']
            assets_d.ManageAccount = self.parame['manageuser']
            assets_d.Port = int(self.parame['port'])
            assets_d.GroupId = self.parame['groupid']
            assets_d.CPU = int(self.parame['cpu'])
            assets_d.MEM = int(self.parame['mem'])
            assets_d.Disk = int(self.parame['disk'])
            assets_d.SystemType = self.parame['systemyype']
            assets_d.SystemVersion = self.parame['systemversion']
            assets_d.HostType = self.parame['hosttype']
            assets_d.OperatEnv = self.parame['operatenv']
            assets_d.HostStatus = self.parame['hoststatus']
            assets_d.Status = int(self.parame['status'])
            assets_d.save()
            self.return_data['code'] = 0
        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "对不起，您提交的信息错误."      
        return self.return_data
    def _deletePerson(self):
        #contact_u = contacts.objects.filter(Uid=self.Data['Uid']).filter(uuid=self.parame["cid"]).first()
        assets_u = assets.objects.filter(uuid=self.parame["cid"])
        if assets_u:
            #print contact_u.uuid
            assets_u.delete()
            self.return_data['code'] = 0
        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "对不起，您提交的信息错误."      
        return self.return_data
        