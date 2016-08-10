# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os,time
#导出数据结构模块
from api.models import *

from lib import NcloudReleaseLib

#操作HandleRelease类
class HandleRelease:

	def __init__(self, Data,params):
		self.params = params
		self.Data = Data
	def GetSiteReleaseList(self):
		#获取当前用户发布站点列表
		LbList = LbInfo.objects.filter(LbZone=self.Data['Zone']).filter(UserId=self.Data['UserId'])
		domainlist = [] 
		lbDomainList = {}
		for lb in LbList:
			LbMonitorList = LbMonitorInfo.objects.filter(LbId=lb.LbId)
			for lbmonitor in LbMonitorList:
				lbDomainList = {"LbDomain":lbmonitor.LbDomain,"siteid":str(lbmonitor.id)}
				domainlist.append(lbDomainList)
		#lbDomainList = json.dumps(lbDomainList)
		return_data = {
			"code" :0,
			"return_data" :domainlist
		}
		return_data = json.dumps(return_data)
		return return_data
	def ReleaseToReady(self):
		#从测试环境获取代码至云平台 目录：/release/UserId/releaseDomain
		downTestStatus = NcloudReleaseLib.TestCodeToNCloud(self.Data,self.params)
		if downTestStatus == 0:
			#压缩上次至云平台的代码(/release/UserId/releaseReady/releaseDomain_time.time().zip)
			version_time = time.time()
			compressedSiteStatus = NcloudReleaseLib.CompressedReleaseCode(self.Data,self.params,version_time)
			if compressedSiteStatus == 0:
				#将压缩包发送至预发布环境 /release/UserId/releaseReady/releaseDomain_time.time().zip c:/WebRoots/niuduz/
				
				#UpReadySiteStatus = NcloudReleaseLib.UpReadyReleaseCode(self.Data,self.params)
				
				#if UpReadySiteStatus == 0:
				ReadyPath = '/release/%s/releaseReady/%s_%s.zip' % (self.Data['UserId'],self.params['releaseDomain'],version_time)
				#插入数据库 站点名、发布至预发布状态、发布至线上状态 版本号 发布人 发布时间 操作
				#如果返回成功则更新当前数据库
				InsertReleaseInfoDB = ReleaseInfo(SiteName=str(self.params['siteName']),ReleaseBewrite=self.params['releaseBewrite'],ReadyStatus=0,LineStatus=0,VersionCode=str(version_time),ReleaseComputerName=self.params['releaseComputer'],ReleaseDomain=self.params['releaseDomain'],ReadyPath=ReadyPath,LinePath='',ReleaseSeedNum=0,Issuer=self.Data['UserEmail'],Zone=self.Data['Zone'],UserId=self.Data['UserId'],SiteId=self.params['siteid'])
				InsertReleaseInfoDB.save()					
				return_data = {
					"code" : 0,
					"msg" : "成功从测试获取代码至云平台，等待预发布环境获取代码。",
					"area" : self.Data['Zone'].lower(),
				}

			else:
				return_data = {
					"code" : 1,
					"msg" : "无法为当前版本存档。",
				}			
		else:
			
			return_data = {
				"code" : 1,
				"msg" : "无法从测试环境获取代码，请查看是否能正常访问。",
			}
		return_data = json.dumps(return_data)
		return return_data
		
	def ModifiedReleaseStatus(self):
		#查询当前releaseID是否存在 如果存在则更新当前releaseID的预发布状态
		if self.params['UpType'] == 0:
			QueryReleaseList = ReleaseInfo.objects.filter(UserId=self.Data['UserId']).filter(id=self.params['ReleaseId'])
		else:
			QueryReleaseList = ReleaseSeedInfo.objects.filter(UserId=self.Data['UserId']).filter(id=self.params['ReleaseId'])
		if QueryReleaseList:
			for QueryRelease in QueryReleaseList:
									
				if QueryRelease.ReadyStatus == 2:
					QueryRelease.LineStatus = 3
					QueryRelease.LineStatusDate = datetime.datetime.now()
					'''
					ReleaseSeedList = ReleaseSeedInfo.objects.filter(ReleaseId=str(QueryRelease.id))
					for ReleaseSeedDetails in ReleaseSeedList:
						ReleaseSeedDetails.LineStatus = 1
						ReleaseSeedDetails.save()
					'''
				else:
					QueryRelease.ReadyStatus = 2
					QueryRelease.ReadyStatusDate = datetime.datetime.now()
					'''
					ReleaseSeedList = ReleaseSeedInfo.objects.filter(ReleaseId=str(QueryRelease.id))
					for ReleaseSeedDetails in ReleaseSeedList:
						ReleaseSeedDetails.ReadyStatus = 0
						ReleaseSeedDetails.save()
					'''
				QueryRelease.save()
			return_data = {
				"code" : 0,
				"msg" : "完成状态更新。",
			}
		else:
			return_data = {
				"code" : 1,
				"msg" : "您提交信息有误，请查询操作是否合理。",
			}
		return_data = json.dumps(return_data)
		return return_data
	def UpReadyRelease(self):
		# ReadyStatus = 0 等待更新至预发布环境，1 已经更新至预发布环境测试中 2 通过测试 3 未通过测试
		#从测试环境获取代码至云平台 目录：/release/UserId/releaseDomain
		#{"action":"UpReadyRelease","siteName":siteName,"releaseBewrite":releaseBewrite,"releaseid":$.getUrlParam("UpId"),"config":config};
		ReleaseDetails = ReleaseInfo.objects.get(id=self.params['releaseid'])
		self.params['releaseComputer'] = ReleaseDetails['ReleaseComputerName']
		self.params['releaseDomain'] = ReleaseDetails['ReleaseDomain']
		downTestStatus = NcloudReleaseLib.TestCodeToNCloud(self.Data,self.params)
		if downTestStatus == 0:
			#压缩上次至云平台的代码(/release/UserId/releaseReady/releaseDomain_time.time().zip)
			version_time = time.time()
			compressedSiteStatus = NcloudReleaseLib.CompressedReleaseCode(self.Data,self.params,version_time)
			if compressedSiteStatus == 0:
				#将压缩包发送至预发布环境 /release/UserId/releaseReady/releaseDomain_time.time().zip c:/WebRoots/niuduz/
				
				#UpReadySiteStatus = NcloudReleaseLib.UpReadyReleaseCode(self.Data,self.params)
				#if UpReadySiteStatus == 0:
				ReadyPath = '/release/%s/releaseReady/%s_%s.zip' % (self.Data['UserId'],self.params['releaseDomain'],version_time)
				#插入数据库 站点名、发布至预发布状态、发布至线上状态 版本号 发布人 发布时间 操作
				#如果返回成功则更新当前数据库
				ReleaseDetails.ReleaseSeedNum = ReleaseDetails.ReleaseSeedNum + 1
				ReleaseDetails.ReadyStatus = 3
				ReleaseDetails.LineStatus = 4
				ReleaseDetails.ReadyStatusDate = datetime.datetime.now()
				ReleaseDetails.LineStatusDate = datetime.datetime.now()
				ReleaseDetails.save()
				ReleaseSeedList = ReleaseSeedInfo.objects.filter(ReleaseId=self.params['releaseid'])
				if ReleaseSeedList:
					for ReleaseSeed in ReleaseSeedList:
						ReleaseSeed.ReadyStatus = 3
						ReleaseSeed.LineStatus = 4
						ReleaseSeed.ReadyStatusDate = datetime.datetime.now()
						#ReleaseSeed.LineStatusDate = datetime.datetime.now()
						ReleaseSeed.save()
				
				InsertReleaseInfoDB = ReleaseSeedInfo(SiteName=self.params['siteName'],ReleaseBewrite=self.params['releaseBewrite'],ReadyStatus=0,LineStatus=0,VersionCode=str(version_time),ReadyPath=ReadyPath,LinePath='',Issuer=self.Data['UserEmail'],Zone=self.Data['Zone'],ReleaseId=self.params['releaseid'],UserId=self.Data['UserId'],SiteId=ReleaseDetails.SiteId,FtpUserName='',FtpPassWord='')
				InsertReleaseInfoDB.save()
				return_data = {
					"code" : 0,
					"msg" : "成功从测试获取代码至云平台，等待预发布环境获取代码。",
					"area" : self.Data['Zone'].lower(),
					"id" : self.params['releaseid'],
				}
			else:
				return_data = {
					"code" : 1,
					"msg" : "无法为当前版本存档。",
				}			
		else:
			
			return_data = {
				"code" : 1,
				"msg" : "无法从测试环境获取代码，请查看是否能正常访问。",
			}
		return_data = json.dumps(return_data)
		return return_data
	def UpReleaseToLine(self):
		#从预发布环境获取代码至云平台 目录：/release/UserId/releaseDomain
		#先判断是父类型还是子类型
		#如果为父类型
		releaseDomain = self.params['releaseDomain']
		if self.params['readytype'] == "0":
			ReleaseDetails = ReleaseInfo.objects.get(id=self.params['releaseid'])
			self.params['releaseComputer'] = ReleaseDetails['ReleaseComputerName']
			self.params['releaseDomain'] = ReleaseDetails['ReleaseDomain']
		else:
			
			ReleaseSeedDetails = ReleaseSeedInfo.objects.get(id=self.params['releaseid'])
			
			ReleaseDetails = ReleaseInfo.objects.get(id=ReleaseSeedDetails.ReleaseId)
			self.params['releaseComputer'] = ReleaseDetails['ReleaseComputerName']
			self.params['releaseDomain'] = ReleaseDetails['ReleaseDomain']

		downReadyStatus = NcloudReleaseLib.ReadyCodeToNCloud(self.Data,self.params,releaseDomain)
		if downReadyStatus == 0:
			#压缩上次至云平台的代码(/release/UserId/releaseLine/releaseDomain_time.time().zip)
			version_time = time.time()
			compressedSiteStatus = NcloudReleaseLib.CompressedReleaseCode(self.Data,self.params,version_time,releaseDomain)
			if compressedSiteStatus == 0:
				#将压缩包发送至线上环境 /release/UserId/releaseLine/releaseDomain_time.time().zip c:/WebRoots/niuduz/
				BackendDetails = BackendInfo.objects.get(id=self.params['backendid'])
				EchDetails = EchInfo.objects.get(EchId=BackendDetails.EchId)
				
				#UpReadySiteStatus = NcloudReleaseLib.UpLineReleaseCode(self.Data,self.params,EchDetails.EchIp)
				#if UpReadySiteStatus == 0:
				ReadyPath = '/release/%s/releaseLine/%s_%s.zip' % (self.Data['UserId'],releaseDomain,version_time)
				#插入数据库 站点名、发布至预发布状态、发布至线上状态 版本号 发布人 发布时间 操作
				#如果返回成功则更新当前数据库
				#ReleaseDetails.ReleaseSeedNum = ReleaseDetails.ReleaseSeedNum + 1
				ReleaseDetails.EchMacs = EchDetails.EchMacs
				ReleaseDetails.ReleaseDomain = releaseDomain
				if self.params['readytype'] == "0":
					ReleaseDetails.LineStatus = 1
					ReleaseDetails.LineUpDate = datetime.datetime.now()
					ReleaseDetails.LinePath = ReadyPath
					#ReleaseDetails.FtpUserName = self.params['ftpuser']
					#ReleaseDetails.FtpPassWord = self.params['ftppwd']
					ReleaseDetails.save()
				else:
					ReleaseSeedList = ReleaseSeedInfo.objects.filter(ReleaseId=ReleaseSeedDetails.ReleaseId)
					
					for ReleaseSeed in ReleaseSeedList:
						if ReleaseSeedDetails.id == ReleaseSeed.id:
							ReleaseSeed.LineStatus = 1
							ReleaseSeedDetails.LineUpDate = datetime.datetime.now()
						else:
							ReleaseSeed.LineStatus = 3
						#ReleaseSeed.FtpUserName = self.params['ftpuser']
						#ReleaseSeed.FtpPassWord = self.params['ftppwd']
						ReleaseSeed.LinePath = ReadyPath
						
						ReleaseSeed.save()
					ReleaseDetails.LineStatus = 3
					ReleaseDetails.save()
				#InsertReleaseInfoDB = ReleaseSeedInfo(SiteName=self.params['siteName'],ReleaseBewrite=self.params['releaseBewrite'],ReadyStatus=0,LineStatus=0,VersionCode=str(version_time),ReadyPath=ReadyPath,LinePath='',Issuer=self.Data['UserEmail'],Zone=self.Data['Zone'],ReleaseId=self.params['releaseid'],UserId=self.Data['UserId'],SiteId=ReleaseDetails.SiteId)
				#InsertReleaseInfoDB.save()
				return_data = {
					"code" : 0,
					"msg" : "发布至线上环境完成",
					"area" : self.Data['Zone'].lower(),
					"id" : self.params['releaseid'],
				}
			else:
				return_data = {
					"code" : 1,
					"msg" : "无法为当前版本存档。",
				}			
		else:
			
			return_data = {
				"code" : 1,
				"msg" : "无法从预发布环境获取代码，请查看是否能正常访问。",
			}
		return_data = json.dumps(return_data)
		return return_data