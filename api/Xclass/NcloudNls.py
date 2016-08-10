# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os,time
#导出数据结构模块
from api.models import *

#from lib import NcloudReleaseLib

#导入hashlib模块
import hashlib
#操作HandleLogs类
class HandleLogs:

	def __init__(self, Data,params):
		self.params = params
		self.Data = Data
	def CreateLogStore(self):
		#判断当前创建的日志库名是否存在。
		LogStoreDetails = LogStoreInfo.objects.filter(UserId=self.Data['UserId']).filter(Zone=self.Data['Zone']).filter(LogStoreName=self.params['LogStoreName'])
		for LogStore in LogStoreDetails:
			print LogStore
		if LogStoreDetails:
			return_data = {
				"code" : 1,
				"msg" : '你当前提交的日志名已存在，请重新添加。',
			}
		else:
			inlogstore = LogStoreInfo(LogStoreName=self.params['LogStoreName'],LogQueryModel=self.params['LogStoreQuery'],LogSaveDay=self.params['savedays'],Zone=self.Data['Zone'],UserId=self.Data['UserId'])
			inlogstore.save()
			return_data = {
				"code" : 0,
				"msg" : '创建成功',
			}
		return_data = json.dumps(return_data)
		return return_data
	def CreateAccess(self):
		KeyID = hashlib.md5(self.Data['UserId']).hexdigest()
		KeySecret = hashlib.sha256(KeyID).hexdigest()
		inaccess = AccessInfo(KeyID=KeyID,KeySecret=KeySecret,AccessStatus=0,KeyUseType='',UserId=self.Data['UserId'])
		inaccess.save()
		return_data = {
			"code" : 0,
			"msg" : '创建成功',
		}
		return_data = json.dumps(return_data)
		return return_data
	def GetSiteReleaseList(self):
		#获取当前用户发布站点列表
		LbList = LbInfo.objects.filter(LbsZone=self.Data['Zone']).filter(UserId=self.Data['UserId'])
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
				UpReadySiteStatus = NcloudReleaseLib.UpReadyReleaseCode(self.Data,self.params)
				if UpReadySiteStatus == 0:
					ReadyPath = '/release/%s/releaseReady/%s_%s.zip' % (self.Data['UserId'],self.params['releaseDomain'],version_time)
					#插入数据库 站点名、发布至预发布状态、发布至线上状态 版本号 发布人 发布时间 操作
					#如果返回成功则更新当前数据库
					InsertReleaseInfoDB = ReleaseInfo(SiteName=str(self.params['siteName']),ReleaseBewrite=self.params['releaseBewrite'],ReadyStatus=0,LineStatus=0,VersionCode=str(version_time),ReleaseComputerName=self.params['releaseComputer'],ReleaseDomain=self.params['releaseDomain'],ReadyPath=ReadyPath,LinePath='',ReleaseSeedNum=0,Issuer=self.Data['UserEmail'],Zone=self.Data['Zone'],UserId=self.Data['UserId'],SiteId=self.params['siteid'])
					InsertReleaseInfoDB.save()					
					return_data = {
						"code" : 0,
						"msg" : "发布至预发布环境完成",
						"area" : self.Data['Zone'].lower(),
					}
				else:
					return_data = {
						"code" : 1,
						"msg" : "无法上传代码至预发布环境。",
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
									
				if QueryRelease.ReadyStatus == 1:
					QueryRelease.LineStatus = 1
					QueryRelease.LineStatusDate = datetime.datetime.now()
					'''
					ReleaseSeedList = ReleaseSeedInfo.objects.filter(ReleaseId=str(QueryRelease.id))
					for ReleaseSeedDetails in ReleaseSeedList:
						ReleaseSeedDetails.LineStatus = 1
						ReleaseSeedDetails.save()
					'''
				else:
					QueryRelease.ReadyStatus = 1
					QueryRelease.ReadyStatusDate = datetime.datetime.now()
					'''
					ReleaseSeedList = ReleaseSeedInfo.objects.filter(ReleaseId=str(QueryRelease.id))
					for ReleaseSeedDetails in ReleaseSeedList:
						ReleaseSeedDetails.ReadyStatus = 1
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
		#从测试环境获取代码至云平台 目录：/release/UserId/releaseDomain
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
				UpReadySiteStatus = NcloudReleaseLib.UpReadyReleaseCode(self.Data,self.params)
				if UpReadySiteStatus == 0:
					ReadyPath = '/release/%s/releaseReady/%s_%s.zip' % (self.Data['UserId'],self.params['releaseDomain'],version_time)
					#插入数据库 站点名、发布至预发布状态、发布至线上状态 版本号 发布人 发布时间 操作
					#如果返回成功则更新当前数据库
					ReleaseDetails.ReleaseSeedNum = ReleaseDetails.ReleaseSeedNum + 1
					ReleaseDetails.ReadyStatus = 2
					ReleaseDetails.LineStatus = 3
					ReleaseDetails.ReadyStatusDate = datetime.datetime.now()
					#ReleaseDetails.LineStatusDate = datetime.datetime.now()
					ReleaseDetails.save()
					ReleaseSeedList = ReleaseSeedInfo.objects.filter(ReleaseId=self.params['releaseid'])
					for ReleaseSeed in ReleaseSeedList:
						ReleaseSeed.ReadyStatus = 2
						ReleaseSeed.LineStatus = 3
						ReleaseSeed.ReadyStatusDate = datetime.datetime.now()
						#ReleaseSeed.LineStatusDate = datetime.datetime.now()
						ReleaseSeed.save()
					InsertReleaseInfoDB = ReleaseSeedInfo(SiteName=self.params['siteName'],ReleaseBewrite=self.params['releaseBewrite'],ReadyStatus=0,LineStatus=0,VersionCode=str(version_time),ReadyPath=ReadyPath,LinePath='',Issuer=self.Data['UserEmail'],Zone=self.Data['Zone'],ReleaseId=self.params['releaseid'],UserId=self.Data['UserId'],SiteId=ReleaseDetails.SiteId)
					InsertReleaseInfoDB.save()
					return_data = {
						"code" : 0,
						"msg" : "发布至预发布环境完成",
						"area" : self.Data['Zone'].lower(),
						"id" : self.params['releaseid'],
					}
				else:
					return_data = {
						"code" : 1,
						"msg" : "无法上传代码至预发布环境。",
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
		print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
		#先判断是父类型还是子类型
		#如果为父类型
		if self.params['readytype'] == "0":
			ReleaseDetails = ReleaseInfo.objects.get(id=self.params['releaseid'])
			self.params['releaseComputer'] = ReleaseDetails['ReleaseComputerName']
			self.params['releaseDomain'] = ReleaseDetails['ReleaseDomain']
		else:
			
			ReleaseSeedDetails = ReleaseSeedInfo.objects.get(id=self.params['releaseid'])
			
			ReleaseDetails = ReleaseInfo.objects.get(id=ReleaseSeedDetails.ReleaseId)
			self.params['releaseComputer'] = ReleaseDetails['ReleaseComputerName']
			self.params['releaseDomain'] = ReleaseDetails['ReleaseDomain']

		downReadyStatus = NcloudReleaseLib.ReadyCodeToNCloud(self.Data,self.params)
		if downReadyStatus == 0:
			#压缩上次至云平台的代码(/release/UserId/releaseLine/releaseDomain_time.time().zip)
			version_time = time.time()
			compressedSiteStatus = NcloudReleaseLib.CompressedReleaseCode(self.Data,self.params,version_time)
			if compressedSiteStatus == 0:
				#将压缩包发送至线上环境 /release/UserId/releaseLine/releaseDomain_time.time().zip c:/WebRoots/niuduz/
				BackendDetails = BackendInfo.objects.get(id=self.params['backendid'])
				EchDetails = EchInfo.objects.get(EchId=BackendDetails.EchId)
				UpReadySiteStatus = NcloudReleaseLib.UpLineReleaseCode(self.Data,self.params,EchDetails.EchIp)
				if UpReadySiteStatus == 0:
					ReadyPath = '/release/%s/releaseLine/%s_%s.zip' % (self.Data['UserId'],self.params['releaseDomain'],version_time)
					#插入数据库 站点名、发布至预发布状态、发布至线上状态 版本号 发布人 发布时间 操作
					#如果返回成功则更新当前数据库
					#ReleaseDetails.ReleaseSeedNum = ReleaseDetails.ReleaseSeedNum + 1
					if self.params['readytype'] == "0":
						ReleaseDetails.LineStatus = 2
						ReleaseDetails.LineUpDate = datetime.datetime.now()
						ReleaseDetails.save()
					else:
						ReleaseSeedList = ReleaseSeedInfo.objects.filter(ReleaseId=ReleaseSeedDetails.ReleaseId)
						for ReleaseSeed in ReleaseSeedList:
							ReleaseSeed.LineStatus = 3
							ReleaseSeed.save()
						ReleaseDetails.LineStatus = 3
						ReleaseSeedDetails.LineStatus = 2
						ReleaseSeedDetails.LineUpDate = datetime.datetime.now()
						ReleaseSeedDetails.save()
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
						"msg" : "无法上传代码至线上环境。",
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