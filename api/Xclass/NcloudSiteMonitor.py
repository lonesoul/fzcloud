# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os
#导出数据结构模块
from api.models import *

from lib import NcloudMonitorLib

#操作Monitor类
class HandleMonitor:

	def __init__(self, Data,params):
		self.params = params
		self.Data = Data
	#创建Monitor类
	
	def CreateHTTPMonitor(self):
		OperateStatus = NcloudMonitorLib.Create_SiteMonitorHTTP(self.Data,self.params)
		return OperateStatus

	def CreateHTTPAlarms(self):
		OperateStatus = NcloudMonitorLib.Create_AlarmsHTTP(self.Data,self.params)
		return OperateStatus
	def GetSiteAlertInfo(self):
		#根据siteId获取数量
		SiteAlertList = CloudAlertInfo.objects.filter(AlertTypeId=self.params['siteid'])
		print len(SiteAlertList)
		#如果查询条件存在 
			#第一 存在一条策略返回第一条MonitorTerm 第二如果存在两条策论则放回不允许创建新策论
		if len(SiteAlertList) > 0:
			if len(SiteAlertList) == 1:
				#返回 code = 0
				#返回 条数
				#返回 MonitorTerm
				#返回状态嘛 返回比较
				for SiteAlertInfo in SiteAlertList:
					MonitorTerm = SiteAlertInfo['MonitorTerm']
					Threshold = SiteAlertInfo['MonitorThreshold']
				Query_resulte = {
					"code" : 0,
					"Alertnum" : len(SiteAlertList),
					"MonitorTerm" : MonitorTerm,
					"Threshold" : Threshold,
				}
				print Query_resulte
			else:
				#返回 code = 0
				#返回 条数
				Query_resulte = {
					"code" : 0,
					"Alertnum" : len(SiteAlertList),
				}
				
		
		#不存在查询条件 返回结果
		else:
			Query_resulte = {
				"code" : 1,
			}
		return Query_resulte
	def CreateContact(self):
		OperateStatus = NcloudMonitorLib.Create_Contact(self.Data,self.params)
		return OperateStatus
	def CreateContactGroup(self):
		OperateStatus = NcloudMonitorLib.Create_ContactGroup(self.Data,self.params)
		return OperateStatus
	def DescribeContactInfo(self):
		OperateStatus = NcloudMonitorLib.GetContactList(self.Data,self.params)
		ContactJson = {
						'code':1,
						'ContactList':OperateStatus,
		}
		ContactJson = json.dumps(ContactJson)
		return ContactJson
	def CreateContactToGroup(self):
		OperateStatus = NcloudMonitorLib.Create_ContactToGroup(self.Data,self.params)
		return OperateStatus
	def EditContactInfo(self):
		OperateStatus = NcloudMonitorLib.Edit_Contact(self.Data,self.params)
		return OperateStatus
	def EditContactGroupInfo(self):
		OperateStatus = NcloudMonitorLib.Edit_ContactGroup(self.Data,self.params)
		return OperateStatus
	def DeleteContact(self):
		OperateStatus = NcloudMonitorLib.Delete_Contact(self.Data,self.params)
		return OperateStatus
	def DeleteContactGroup(self):
		OperateStatus = NcloudMonitorLib.Delete_ContactGroup(self.Data,self.params)
		return OperateStatus