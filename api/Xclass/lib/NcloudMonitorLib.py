# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os
#导出数据结构模块
from api.models import *
from api.ManagerEch import *
#操作cache类
def Create_SiteMonitorHTTP(Data,params):
	if len(params['SubContent']) == 0:
		SubContent = ''
	else:
		SubContent = json.dumps(params['SubContent'])
	if len(params['HTTPHeader']) == 0:
		HTTPHeader = ''
	else:
		HTTPHeader = json.dumps(params['HTTPHeader'])
	inSiteMonitor = SiteMonitorHttpInfo(MonitorName=params['MonitorSiteName'],MonitorAddress=params['MonitorSiteAdd'],MonitorTerm=params['MonitorTerm'],MonitorRequestType=params['MonitorRequestType'],MonitorPath=params['MonitorSitePath'],MonitorHeader=HTTPHeader,MonitorRequestContent=SubContent,MonitorType=params['MonitorType'],UserId=Data['UserId'])
	inSiteMonitor.save()
	return 'done'
def Create_AlarmsHTTP(Data,params):
	#获取监控频率
	siteMonitorList = SiteMonitorHttpInfo.objects.get(id=params['siteid'])
	print siteMonitorList['MonitorTerm']
	if params['ResponseTimethreshold'] == 0:
		if params['code'] == 1:
			pass
		else:
			inCloudAlert = CloudAlertInfo(MonitorName='',MonitorTerm='http.status',StatisticalCycle=siteMonitorList['MonitorTerm'],StatisticalMethod="average",MonitorCompare=params['compare'],MonitorThreshold=params['threshold'],AlertRepeatNumber=params['repeat_number'],AlertNum=1,AlertContactGroup=params['contactgroup'],AlertType='HTTP',AlertTypeId=params['siteid'],UserId=Data['UserId'])
	#inSiteMonitor = SiteMonitorHttpInfo(MonitorName=params['MonitorSiteName'],MonitorAddress=params['MonitorSiteAdd'],MonitorTerm=params['MonitorTerm'],MonitorRequestType=params['MonitorRequestType'],MonitorPath=params['MonitorSitePath'],MonitorHeader=HTTPHeader,MonitorRequestContent=SubContent,MonitorType=params['MonitorType'],UserId=Data['UserId'])
			inCloudAlert.save()
	else:
		if params['code'] == 2:
			inhCloudAlert = CloudAlertInfo(MonitorName='',MonitorTerm='http.status',StatisticalCycle=siteMonitorList['MonitorTerm'],StatisticalMethod="average",MonitorCompare=params['compare'],MonitorThreshold=params['threshold'],AlertRepeatNumber=params['repeat_number'],AlertNum=1,AlertContactGroup=params['contactgroup'],AlertType='HTTP',AlertTypeId=params['siteid'],UserId=Data['UserId'])
			inhCloudAlert.save()
			inrCloudAlert = CloudAlertInfo(MonitorName='',MonitorTerm='http.responetime',StatisticalCycle=siteMonitorList['MonitorTerm'],StatisticalMethod="average",MonitorCompare=params['compare'],MonitorThreshold=params['threshold'],ResponeTime=params['ResponseTimethreshold'],AlertRepeatNumber=params['repeat_number'],AlertNum=1,AlertContactGroup=params['contactgroup'],AlertType='HTTP',AlertTypeId=params['siteid'],UserId=Data['UserId'])
			inrCloudAlert.save()
		elif params['code'] == 1:
			inrCloudAlert = CloudAlertInfo(MonitorName='',MonitorTerm='http.responetime',StatisticalCycle=siteMonitorList['MonitorTerm'],StatisticalMethod="average",MonitorCompare=params['compare'],MonitorThreshold=params['threshold'],ResponeTime=params['ResponseTimethreshold'],AlertRepeatNumber=params['repeat_number'],AlertNum=1,AlertContactGroup=params['contactgroup'],AlertType='HTTP',AlertTypeId=params['siteid'],UserId=Data['UserId'])
			inrCloudAlert.save()
		else:
			inhCloudAlert = CloudAlertInfo(MonitorName='',MonitorTerm='http.status',StatisticalCycle=siteMonitorList['MonitorTerm'],StatisticalMethod="average",MonitorCompare=params['compare'],MonitorThreshold=params['threshold'],AlertRepeatNumber=params['repeat_number'],AlertNum=1,AlertContactGroup=params['contactgroup'],AlertType='HTTP',AlertTypeId=params['siteid'],UserId=Data['UserId'])
			inhCloudAlert.save()
		
	return 'done'

def Create_Contact(Data,params):
	#创建联系人
	ContactList = ContactInfo.objects.filter(ContactEmail=params['ContactEmail']).filter(UserId=Data['UserId'])
	if ContactList:
		return 0
	else:
		inContact = ContactInfo(ContactName=params['ContactName'],ContactMobile=params['ContactMobile'],ContactEmail=params['ContactEmail'],UserId=Data['UserId'])
		inContact.save()
		return 1

def Create_ContactGroup(Data,params):
	#查询当前提交群组名称是否存在
	ContactGroupList = ContactGroupInfo.objects.filter(ContactGroupName=params['ContactGroupName'].strip())
	#如果存在则放回不可创建
	if ContactGroupList:
		return 0
	#否则创建群组
	else:
		inContactGroup = ContactGroupInfo(ContactGroupName=params['ContactGroupName'],ContactGroupBewrite=params['ContactGroupBewrite'],UserId=Data['UserId'])
		inContactGroup.save()
		return 1
		
def GetContactList(Data,params):
		
	ContactList = ContactInfo.objects.filter(UserId=Data['UserId'])
	ContactToGroup =[]
	for Contact in ContactList:

		#获取组id  
		ContactGroup = ContactGroupInfo.objects.get(ContactGroupName=params['ContactName'])
		#当前用户是否属于当前组
		
		CheckContactStatus = ContactgroupToContactInfo.objects.filter(ContactGroupId=str(ContactGroup['id'])).filter(ContactId=str(Contact['id']))
		if CheckContactStatus:
			checkStatus = 1
		else:
			checkStatus = 0
		ContactInfoList ={"ContactName":Contact['ContactName'],"ContactId":str(Contact['id']),"checkStatus":checkStatus}
		ContactToGroup.append(ContactInfoList)
	return ContactToGroup


def Create_ContactToGroup(Data,params):
	#获取联系人组id
	ContactGroup = ContactGroupInfo.objects.get(ContactGroupName=params['ContactName'])
	ContactGroupId = str(ContactGroup['id'])
	#查询用户组下的用户
	ContactToGroupList = ContactgroupToContactInfo.objects.filter(ContactGroupId=ContactGroupId)
	#判断提交的用户数 如果为空 删除当前用户组下的所有用户
	if len(params['userlist']) == 0:
		ContactToGroupList.delete() 
		return 1
	#继续查询
	else:
		ContactList = params['userlist'].split('|')
		try:
			if ContactList[1]:
				for Contact in ContactList:
					print Contact
					ContactStatus = ContactgroupToContactInfo.objects.filter(ContactGroupId=ContactGroupId).filter(ContactId=Contact)
					if ContactStatus:
						pass
					else:
						print '1bbbbbbbbbbbbbbbbbbbbbbbbb'
						inContactToGroup = ContactgroupToContactInfo(ContactGroupId=ContactGroupId,ContactId=Contact)
						inContactToGroup.save()
		except:
			ContactStatus = ContactgroupToContactInfo.objects.filter(ContactGroupId=ContactGroupId).filter(ContactId=ContactList[0])
			if ContactStatus:
				pass
			else:
				inContactToGroup = ContactgroupToContactInfo(ContactGroupId=ContactGroupId,ContactId=ContactList[0])
				inContactToGroup.save()
		ContactToGroupList = ContactgroupToContactInfo.objects.filter(ContactGroupId=ContactGroupId)
		for ContactToGroup in ContactToGroupList:
			try:
				ContactVali = ContactList.index(ContactToGroup['ContactId'])
				if str(ContactVali):
					ContactNum = 1
				else:
					ContactNum = 0
			except:
				if ContactToGroup['ContactId'] == ContactList[0]:
					ContactNum = 1
				else:
					ContactNum = 0
			if ContactNum == 0:
				delContactToGroup = ContactgroupToContactInfo.objects.get(ContactId=ContactToGroup['ContactId'])
				delContactToGroup.delete()
		return 1
def Edit_Contact(Data,params):
	#查询当前用户下Contactid 是否存在 如果存在继续 如果不存在pass
	ContactDetails = ContactInfo.objects.filter(UserId=Data['UserId']).filter(id=params['contactid'])
	if ContactDetails:
		for ContactDetail in ContactDetails:
			ContactDetail.ContactName = params['ContactName']
			
			ContactDetail.ContactMobile = params['ContactMobile']
			if ContactDetail.ContactEmail == params['ContactEmail']:
				pass
			else:
				#查询是否存在 如果存在 return 0 
				ContactList = ContactInfo.objects.filter(ContactEmail=params['ContactEmail']).filter(UserId=Data['UserId'])
				if ContactList:
					return 0 
				else:
					ContactDetail.ContactEmail = params['ContactEmail']
			ContactDetail.save()
		return 1
	else:
		return 0
def Edit_ContactGroup(Data,params):
	#查询当前用户下联系组名 是否存在 如果存在pass 如果不存在继续
	#查询当前用户下Contactid 是否存在 如果存在继续 如果不存在pass
	ContactGroupDetails = ContactGroupInfo.objects.filter(ContactGroupName=params['ycontactgroupname']).filter(UserId=Data['UserId'])
	if ContactGroupDetails:
		for ContactGroupDetail in ContactGroupDetails:
			ContactGroupDetail.ContactGroupBewrite = params['ContactGroupBewrite']
			if ContactGroupDetail.ContactGroupName == params['ContactGroupName']:
				pass
			else:
				#查询是否存在 如果存在 return 0 
				ContactGroupList = ContactGroupInfo.objects.filter(ContactGroupName=params['ContactGroupName']).filter(UserId=Data['UserId'])
				if ContactGroupList:
					return 0 
				else:
					ContactGroupDetail.ContactGroupName = params['ContactGroupName']
			ContactGroupDetail.save()
		return 1
	else:
		return 0

def Delete_Contact(Data,params):
	#删除当前用户
	print params['contactid']
	Contactlist = ContactInfo.objects.get(id=params['contactid'])
	Contactlist.delete()
	#删除组下的用户
	AlertContactList = ContactgroupToContactInfo.objects.filter(ContactId=params['contactid'])
	AlertContactList.delete()
	return 1
def Delete_ContactGroup(Data,params):
	#删除当前用户组，查询当前用户组是否存在
	ContactGrouplist = ContactGroupInfo.objects.filter(ContactGroupName=params['contactgroupname']).filter(UserId=Data['UserId'])
	if ContactGrouplist:
		for ContactGroupDetail in ContactGrouplist:
			ContactGroupId = str(ContactGroupDetail.id)
			CloudAlertDetail = CloudAlertInfo.objects.filter(AlertContactGroup=ContactGroupId)
			if CloudAlertDetail:
				return 0
			else:
			#删除组下的用户
				AlertContactList = ContactgroupToContactInfo.objects.filter(ContactGroupId=ContactGroupId)
				AlertContactList.delete()
				ContactGroupDetail.delete()
		return 1
	else:
		return 0