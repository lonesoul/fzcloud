#!/usr/bin/env python
# *-* coding: utf-8 *-*

import datetime

from api.models import contacts,cgroups,c_group
from api.lib import XcloudLib
from uuid import uuid1
class ContactHandle(object):

    """
    """
    def __init__(self,parame,Data):
        self.parame = parame
        self.Data = Data
        self.return_data = {}
    def Person(self):
        return_data = {}
        if self.parame['action'] == 'addPerson':self._addPerson()
        elif self.parame['action'] == 'updatePerson':self._updatePerson()
        elif self.parame['action'] == 'deletePerson':self._deletePerson()
        elif self.parame['action'] == 'addContact':self._addContact()
        elif self.parame['action'] == 'newGroup':self._newGroup()
        elif self.parame['action'] == 'addDetailPerson':self._addDetailPerson()
        elif self.parame['action'] == 'addContactToGroup':self._addContactToGroup()
        elif self.parame['action'] == 'deleteContactToGroup':self._deleteContactToGroup()
        elif self.parame['action'] == 'deleteCGroup':self._deleteCGroup()
        return self.return_data
    def _deleteCGroup(self):
    
        cgroups_n = cgroups.objects.filter(uuid=self.parame["gid"])
        if cgroups_n:
            c_group.objects.filter(C_Groupid=self.parame["gid"]).delete()
            cgroups_n.delete()
            self.return_data['code'] = 0
        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "对不起，您提交的信息错误."      
        return self.return_data
    def _deleteContactToGroup(self):
        #contact_u = contacts.objects.filter(Uid=self.Data['Uid']).filter(uuid=self.parame["cid"]).first()
        contact_u = c_group.objects.filter(C_Groupid=self.parame["cgroupsId"]).filter(Contactid=self.parame["cid"])
        if contact_u:
            #print contact_u.uuid
            contact_u.delete()
            cgroups_n = cgroups.objects.filter(uuid=self.parame["cgroupsId"]).first()
            cgroups_n.ContactNum = cgroups_n.ContactNum -1
            cgroups_n.save()
            self.return_data['code'] = 0
        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "对不起，您提交的信息错误."      
        return self.return_data
    def _addContactToGroup(self):
        #严重联系组id是否存在存在则插入联系人关系表
        contact_g = cgroups.objects.filter(Uid=self.Data['Uid']).filter(uuid=self.parame['cgroupsId']).first()
        if contact_g:
            '''
            print self.parame['name']
            print self.parame['phone']
            print datetime.datetime.now()
            '''
            
            for cid in self.parame["clist"]:
                print cid
                c_group(C_Groupid=self.parame['cgroupsId'],
                        Contactid=cid,
                        Uid=self.Data['Uid']).save()
            contact_g.ContactNum = contact_g.ContactNum + len(self.parame["clist"])
            contact_g.save()
            self.return_data['code'] = 0
            self.return_data['msg'] = "添加联系人成功."   

        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "您输入的联系组已经存在."
        return self.return_data      
    def _addDetailPerson(self):
        contact_u = contacts.objects.filter(Uid=self.Data['Uid'])
        c_g_list = c_group.objects.filter(C_Groupid=self.parame['cgid'])
        cg_list = []
        for cg_details in c_g_list:
            cg_list.append(cg_details.Contactid)
        data = []
        for contact_details in contact_u:
            if contact_details.uuid in cg_list:pass
            else:
                contact_d = {}
                contact_d["cid"] = contact_details.uuid
                contact_d["name"] = contact_details.Name
                contact_d["phone"] = contact_details.Phone
                contact_d["email"] = contact_details.Email
                data.append(contact_d)
        self.return_data['data'] = data
        self.return_data["code"] = 0
        
        return self.return_data
    def _newGroup(self):
        contact_g = cgroups.objects.filter(Name=self.parame['grourName'])
        if contact_g:
            self.return_data['code'] = 10000
            self.return_data['msg'] = "您输入的联系组已经存在."
        else:
            '''
            print self.parame['name']
            print self.parame['phone']
            print datetime.datetime.now()
            '''
            print self.Data['Uid']
            c_g = cgroups(uuid=uuid1(),
                              Name=self.parame['grourName'],
                              ContactNum=len(self.parame['clist']),
                              Uid=self.Data['Uid'])
            c_g.save()
            for cid in self.parame["clist"]:
                c_group(C_Groupid=c_g.uuid,
                        Contactid=cid,
                        Uid=self.Data['Uid']).save()
            self.return_data['code'] = 0
            self.return_data['msg'] = "添加联系人成功."       
        return self.return_data        
    
    
    def _addContact(self):
        contact_u = contacts.objects.filter(Uid=self.Data['Uid'])

        data = []
        for contact_details in contact_u:
            if contact_details.uuid in self.parame['clist']:pass
            else:
                contact_d = {}
                contact_d["cid"] = contact_details.uuid
                contact_d["name"] = contact_details.Name
                contact_d["phone"] = contact_details.Phone
                contact_d["email"] = contact_details.Email
                data.append(contact_d)
        self.return_data['data'] = data
        self.return_data["code"] = 0
        
        return self.return_data
    
    def _addPerson(self):
        contact_u = contacts.objects.filter(Phone=self.parame['phone'],
                                            Email=self.parame['email']
                                            ).first()
        if contact_u:
            self.return_data['code'] = 10000
            self.return_data['msg'] = "您输入的联系人信息已经存在."
        else:
            '''
            print self.parame['name']
            print self.parame['phone']
            print datetime.datetime.now()
            '''
            contacts(uuid=uuid1(),
                     Name=self.parame['name'],
                     Email=self.parame['email'],
                     Phone=self.parame['phone'],
                     Uid=self.Data['Uid']).save()
            self.return_data['code'] = 0
            self.return_data['msg'] = "添加联系人成功."       
        return self.return_data
        
    def _updatePerson(self):
        
        contact_u = contacts.objects.filter(Uid=self.Data['Uid']).filter(uuid=self.parame["nowId"]).first()

        if contact_u:
            contact_u.Name = self.parame['name']
            contact_u.Phone = self.parame['phone']
            contact_u.Email = self.parame['email']
            contact_u.save()
            self.return_data['code'] = 0
        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "对不起，您提交的信息错误."      
        return self.return_data
    def _deletePerson(self):
        #contact_u = contacts.objects.filter(Uid=self.Data['Uid']).filter(uuid=self.parame["cid"]).first()
        contact_u = contacts.objects.filter(uuid=self.parame["cid"])
        if contact_u:
            #print contact_u.uuid
            contact_u.delete()
            self.return_data['code'] = 0
        else:
            self.return_data['code'] = -1
            self.return_data['msg'] = "对不起，您提交的信息错误."      
        return self.return_data
        