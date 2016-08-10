# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os,time
#导出数据结构模块
from api.models import *

from lib import NcloudNlbLib
from lib import NcloudLib
from api.ManagerEch import *
#导入hashlib模块
import hashlib,uuid
#操作HandleNlb类
class HandleNlb:

	def __init__(self, Data,params):
		self.params = params
		self.Data = Data
	def CreateLB(self):
		#计算LbId
		LbUUID = str(uuid.uuid1())
		LbId = 'lb-' + LbUUID[:8]
		eipgroup = EipInfo.objects.get(id=self.params['eip'])
		eipgroup.AssignType = 1
		eipgroup.AssignId = LbUUID
		EipId = eipgroup.EipId
		EipGroup = eipgroup.EipGroup
		IpsId = eipgroup.EipAddressId
		#如果用户类型等于3，则直接插入数据
		if self.Data['UserType'] != 3:
			#查询Lvsinfo表
			#查询当前区域是否有LVS集群 有继续 无返回结果
			Lvs_List = LvsInfo.objects.filter(LvsZone=self.Data['Zone'])

			if Lvs_List:
				#print '存在'
				LVSHandles = []
				LVSStatus = 0
				for LvsDetails in Lvs_List:
					LvsHandleInfo = {
						'id' : str(LvsDetails['id']),
						'LvsWeight' : LvsDetails['LvsWeight'],
						'LvsIp' : LvsDetails['LvsIp'],
						'GroupId' : LvsDetails['GroupId'],
					}
					LVOperateOut = NcloudLib.HttpRequest({'action':'LVSStatus'},LvsDetails['LvsIp'],35796)
					print LVOperateOut
					LVSStatus = int(LVOperateOut['code'])
					VrrpNum = LvsDetails['VrrpNum']
					LVSHandles.append(LvsHandleInfo)
				#判断LVS集群组状态是否正常  正常继续 不正常返回结果
				if LVSStatus == 0:
					print IpsId
					Lbs_List = LbsInfo.objects.filter(IpsId=IpsId)
					if Lbs_List:
						print '存在Lbs'
						#存在负载 则为查询结果中lbsweight 1为主 0为备
						NLBHandleInfo = []
						NLBStatus = 0
						NLBIPs = []
						for LbsDetail in Lbs_List:
							LbsHandleInfo = {
								'LbsWeight' : LbsDetail['LbsWeight'],
								'LbsIp' : LbsDetail['LbsIp'],
								'id' : LbsDetail['id'],
								'GroupId' : LbsDetail['GroupId'],
							}
							
							#获取相对主备ip
							#获取当前负载主机状态
							LBOperateOut = NcloudLib.HttpRequest({'action':'NLBStatus'},LbsDetail['LbsIp'],35796)
							NLBStatus = int(LBOperateOut['code'])
							NLBIPs.append(LbsDetail['LbsIp'])
							NLBHandleInfo.append(LbsHandleInfo)
						#如果NLBStatus=0 负载集群组存活
						if NLBStatus == 0:
							if EipGroup == 1:
								#双线IP
								#获取VID和Rid
								#根据VrrpNum 计算ViD和Rid 当前值 T+1 U+2 更新VrrpNum+2
								TVrrpNum = VrrpNum + 1
								UVrrpNum = VrrpNum + 2
								KVrrpNum = VrrpNum + 2
								Tip = self.params['eips'].split(',')[0]
								Uip = self.params['eips'].split(',')[1]
								parame = {
									'TVrrpNum' : TVrrpNum,
									'UVrrpNum' : UVrrpNum,
									'Tip' : Tip,
									'Uip' : Uip,
								}
							#获取KEEPLIVED配置文件
							LvsCfg = NcloudNlbLib.GetDoubletLvsCfg(parame)
							#获取NLB-Server配置文件
							#LbCfg = NcloudNlbLib.GetDoubletCreateLBCfg(NLBHandleInfo)
							for LVSHandle in LVSHandles:
								if LVSHandle['LvsWeight'] == 1:
									operateinfo = {
										'action':'CreateLVS',
										'parame' : {
											'Keepalived' : LvsCfg['keepalivedM'],
											'LBroute' : LvsCfg['LBroute'],
											'FileLvsName' : self.params['eips'],
											'Eips' : [Tip,Uip],
										}
									}
									LvsId = LVSHandle['id']
									LvsGroupId = LVSHandle['GroupId']
								else:
									operateinfo = {
										'action':'CreateLVS',
										'parame' : {
											'Keepalived' : LvsCfg['keepalivedB'],
											'LBroute' : LvsCfg['LBroute'],
											'FileLvsName' : self.params['eips'],
											'Eips' : [Tip,Uip],
										}
									}
								print operateinfo
								LVSOperateOut = NcloudLib.HttpRequest(operateinfo,LVSHandle['LvsIp'],35796)
								print LVSOperateOut
								if LVSOperateOut['code'] == 0:
									CreateLvsStatus = 1
								else:
									CreateLvsStatus = 0
							CreateLBStatus = 1
							'''
							for NLBHandle in NLBHandleInfo:
								operateinfo = {
										'action':'CreateLB',
										'parame': {
											'LBserver' : LbCfg['LBserver'],
											'FileServerName' : NLBHandle['LbsIp'],
										},
									}
								print operateinfo
								#LBOperateOut = Operate(NLBHandle['LbsIp'],operateinfo)
								print LBOperateOut
								if 'done' == 'done':
									CreateLBStatus = 1
								else:
									CreateLBStatus = 0
							'''
							if CreateLBStatus == 1 and CreateLvsStatus == 1:
								#更新LVS相对主备
								for LvsDetails in Lvs_List:
									if LvsDetails['LvsWeight'] == 1:
										LvsDetails.LvsWeight = 2
									else:
										LvsDetails.LvsWeight = 1
									LvsDetails.VrrpNum = KVrrpNum
									
									LvsDetails.save()
								inLb = LbInfo(LbId=LbId,LbName=self.params['LBName'],LbType=self.params['LBType'],LbIp=self.params['eips'],EipId=self.params['eip'],LbContNum=5000,LbZone=self.Data['Zone'],LvsId=LvsId,LvsGroupId=LvsGroupId,LbPaymentType=0,LbPaymentDate=0,IpsId=IpsId,LbUUID=LbUUID,UserId=self.Data['UserId'])
								inLb.save()
								eipgroup.save()
								return_data = {
									'code' : 0,
									'msg' : '您已提交成功，稍等片刻，8号就能为您服务了。',
								}
							else:
								return_data = {
									'code' : 1001,
									'msg' : '创建失败，请您重新在多戳几次鼠标或联系客服妹子。',
								}
						else:
							return_data = {
								'code' : 1,
								'msg' : '创建失败，请您重新在多戳几次鼠标或联系客服妹子1。',
							}
					else:
						'''
						print '不存在Lbs'
						#不存在更改预备负载集群状态
						#获取是否存在预备负载集群  存在 获取LbsWeight = 0 为主 并变更状态为1   不存在则返回
						Lbs_ready_List = LbsInfo.objects.filter(LbsStatus=0).filter(LbsZone=self.Data['Zone']).filter(GroupId=0)
						if Lbs_ready_List:
							NLBHandleInfo = []
							NLBStatus = 0
							#计算LBSGroupID = 
							LbsGroupIdList = LbsInfo.objects.filter()
							LbsGroupId = len(LbsGroupIdList)/2
							for LbsDetail in Lbs_ready_List:
								LbsHandleInfo = {
									'LbsWeight' : LbsDetail['LbsWeight'],
									'LbsIp' : LbsDetail['LbsIp'],
									'id' : LbsDetail['id'],
								}
								if LbsDetail['LbsWeight'] == 1:
									LbsId = str(LbsDetail['id'])
								#获取相对主备ip
								LBOperateOut = Operate(LbsDetail['LbsIp'],{'action':'NLBStatus'})
								
								NLBStatus = int(LBOperateOut)
								NLBHandleInfo.append(LbsHandleInfo)

							if NLBStatus == 0:
								if EipGroup == 1:
									#双线IP
									#获取VID和Rid
									#根据VrrpNum 计算ViD和Rid 当前值 T+1 U+2 更新VrrpNum+2
									TVrrpNum = VrrpNum + 1
									UVrrpNum = VrrpNum + 2
									KVrrpNum = VrrpNum + 2
									Tip = self.params['eips'].split(',')[0]
									Uip = self.params['eips'].split(',')[1]
									parame = {
										'TVrrpNum' : TVrrpNum,
										'UVrrpNum' : UVrrpNum,
										'Tip' : Tip,
										'Uip' : Uip,
									}
								#获取KEEPLIVED配置文件
								LvsCfg = NcloudNlbLib.GetDoubletLvsCfg(parame)
								#获取NLB-Server配置文件
								LbCfg = NcloudNlbLib.GetDoubletCreateLBCfg(NLBHandleInfo)
								for LVSHandle in LVSHandles:
									if LVSHandle['LvsWeight'] == 1:
										operateinfo = {
											'action':'CreateLVS',
											'parame' : {
												'Keepalived' : LvsCfg['keepalivedM'],
												'LBroute' : LvsCfg['LBroute'],
												'FileLvsName' : self.params['eips'],
												'Eips' : [Tip,Uip],
											}
										}
										LvsId = LVSHandle['id']
										LvsGroupId = LVSHandle['GroupId']
									else:
										operateinfo = {
											'action':'CreateLVS',
											'parame' : {
												'Keepalived' : LvsCfg['keepalivedB'],
												'LBroute' : LvsCfg['LBroute'],
												'FileLvsName' : self.params['eips'],
												'Eips' : [Tip,Uip],
											}
										}
									print operateinfo
									LVSOperateOut = Operate(LVSHandle['LvsIp'],operateinfo)
									print LVSOperateOut
									if LVSOperateOut == 'done':
										CreateLvsStatus = 1
									else:
										CreateLvsStatus = 0
								
								for NLBHandle in NLBHandleInfo:
									operateinfo = {
											'action':'CreateLB',
											'parame': {
												'LBserver' : LbCfg['LBserver'],
												'FileServerName' : self.params['eips'],
												'NetLo' : NetLo,
											},
										}
									print operateinfo
									#LBOperateOut = Operate(NLBHandle['LbsIp'],operateinfo)
									#print LBOperateOut
									
									if 'done' == 'done':
										CreateLBStatus = 1
									else:
										CreateLBStatus = 0
										
								if CreateLBStatus == 1 and CreateLvsStatus == 1:
									#更新当前相对主的状态
									for LbsStatusInfo in Lbs_ready_List:
										LbsStatusInfo.GroupId = LbsGroupId
										LbsStatusInfo.save()
									for LvsDetails in Lvs_List:
										if LvsDetails['LvsWeight'] == 1:
											LvsDetails.LvsWeight = 2
										else:
											LvsDetails.LvsWeight = 1
										LvsDetails.VrrpNum = KVrrpNum
										
										LvsDetails.save()
									LbsStatusEdit = LbsInfo.objects.get(id=LbsId)
									LbsStatusEdit.LbsStatus = 1
									LbsStatusEdit.save()
									inLb = LbInfo(LbId=LbId,LbName=self.params['LBName'],LbType=self.params['LBType'],LbIp=self.params['eips'],EipId=self.params['eip'],LbContNum=5000,LbsZone=self.Data['Zone'],LbsId=LbsId,LbsGroupId=LbsGroupId,LvsId=LvsId,LvsGroupId=LvsGroupId,LbPaymentType=0,LbPaymentDate=0,UserId=self.Data['UserId'])
									inLb.save()
									eipgroup.save()
									
									return_data = {
										'code' : 0,
										'msg' : '您已提交成功，稍等片刻，8号就能为您服务了。',
									}
								else:
									return_data = {
										'code' : 10010,
										'msg' : '创建失败，请您重新在多戳几次鼠标或联系客服妹子1。',
									}
							else:
								return_data = {
									'code' : 1001,
									'msg' : '创建失败，请您重新在多戳几次鼠标或联系客服妹子1。',
								}
						'''
						return_data = {
								'code' : 1001,
								'msg' : '创建失败，请您重新在多戳几次鼠标或联系客服妹子。',
						}
				else:
					print '暂时无法操作'
					return_data = {
						'code' : 1,
						'msg' : '创建失败，请您重新在多戳几次鼠标或联系客服妹子。',
					}
			else:
				#print '不存在'
				return_data = {
					'code' : 10010,
					'msg' : '对不起，您提交的区域暂时无法为您创建负载均衡。',
				}
			
		else:
			#用户类型==3 调用统一的NLB 直接插入数据
	
			inLb = LbInfo(LbId=LbId,LbName=self.params['LBName'],LbType=self.params['LBType'],LbIp=self.params['eips'],EipId=self.params['eip'],LbContNum=5000,LbZone=self.Data['Zone'],LvsId='',LvsGroupId=1,LbPaymentType=0,LbPaymentDate=0,IpsId=IpsId,LbUUID=LbUUID,UserId=self.Data['UserId'])
			inLb.save()
			eipgroup.save()
			return_data = {
				'code' : 0,
				'msg' : '您已提交成功，稍等片刻，8号就能为您服务了。',
			}
		return_data = json.dumps(return_data)
		return return_data
	def CreateLbBackend(self):
		VswDetails = VpcSwitch.objects.get(VswId=self.params['vswid'])
		VrtDetails = VpcRouter.objects.get(TenantId=VswDetails.TenantId)
		
		BackendList = BackendInfo.objects.filter(LbMonitorId=self.params['LbUpstreamId']).filter(TenantId=VswDetails.TenantId).filter(BackendPort=self.params['BackendPort'])
		if BackendList:
			code = 1
			msg = '您提交的已提交，请修改后重新提交'
		else:
			#获取ECH IPAddress
			EchList = EchInfo.objects.get(EchId=self.params['EchId'])
			EchIp = EchList.EchIp
			BackendPort = self.params['BackendPort']
			BackendWeight = self.params['BackendWeight']
			#获取LBMonitor domain,port,LbProtocol
			LbMonitorList = LbMonitorInfo.objects.get(id=self.params['LbUpstreamId'])
			LbDomain = LbMonitorList.LbDomain
			UpstreamName = LbDomain.replace('.','')
			listener_port = LbMonitorList.LbPort
			LbProtocol = LbMonitorList.LbProtocol
			RouterEips = VrtDetails.RouterEips
			BackendDetails = BackendInfo.objects.filter(LbMonitorId=self.params['LbUpstreamId'])
			BackendNum = len(BackendDetails)
			#创建Backend
			ServerBackend = """server %s:%s weight=%s;\n""" % (RouterEips,BackendPort,BackendWeight)
			operateinfo = {
				'action':'CreateLbBackend',
				'parame':{
					'FileName':UpstreamName+str(listener_port),
					'ServerBackend':ServerBackend,
					"BackendNum":BackendNum,
				},
			}
			LbDetails = LbInfo.objects.get(LbId=self.params['loadbalancerid'])
			LbsList = LbsInfo.objects.filter(IpsId=LbDetails['IpsId'])
			if LbsList:
				#获取负载集群状态
				NLBHandleInfo = []
				NLBStatus = 0
				for LbsDetail in LbsList:
					LbsHandleInfo = {
						'LbsWeight' : LbsDetail['LbsWeight'],
						'LbsIp' : LbsDetail['LbsIp'],
					}
					#获取相对主备ip
					LBOperateOut = NcloudLib.HttpRequest({'action':'NLBStatus'},LbsDetail['LbsIp'],35796)
					NLBStatus = int(LBOperateOut['code'])
					
					NLBHandleInfo.append(LbsHandleInfo)
				if NLBStatus == 0:
					for LbsDetail in LbsList:
						LbsIp = LbsDetail.LbsIp
						print operateinfo
						BackendOperateOut = NcloudLib.HttpRequest(operateinfo,LbsDetail['LbsIp'],35796)
						print BackendOperateOut
						if BackendOperateOut['code'] == 0:
							BackendStatus = 1
						else:
							BackendStatus = 0
					if BackendStatus == 1:
						inBackend = BackendInfo(BackendName=self.params['BackendName'],BackendIp=EchIp,BackendPort=BackendPort,LbProtocol=LbProtocol,BackendWeight=BackendWeight,EchId=self.params['EchId'],TenantId=VswDetails.TenantId,RouterEips=RouterEips,LbMonitorId=self.params['LbUpstreamId'],LbId=self.params['loadbalancerid'])
						inBackend.save()
						code = 0
						msg = '创建成功。'
					else:
						code = 0
						msg = '暂时无法为您添加后端负载，请您稍后提交或联系客服。'
			else:
				code = 10010
				msg = '暂时无法为您添加后端负载，请您稍后提交或联系客服。'
		return_data = {
			'code' : code,
			'msg' : msg,
		}
		return_data = json.dumps(return_data)
		return return_data
	def ForbiddenBankend(self):
		#根据条件查询列表 存在继续执行 不存在返回结果
		
		#try:
		
		BackendDetails = BackendInfo.objects.get(id=self.params['BackendId'])
		ServerBackend = 'server %s:%s weight=%s;' % (BackendDetails['RouterEips'],BackendDetails['BackendPort'],BackendDetails['BackendWeight'])
		LbMonitorDetail = LbMonitorInfo.objects.get(id=BackendDetails['LbMonitorId'])
		UpstreamName = LbMonitorDetail['LbDomain'].replace('.','')
		operateinfo = {
			'action':'ForbiddenBankend',
			'parame':{
				'FileName':UpstreamName+str(LbMonitorDetail['LbPort']),
				'ServerBackend':ServerBackend,
			},
		}
		if BackendDetails:
			#获取LbsGroupId
			LbDetails = LbInfo.objects.get(LbId=BackendDetails['LbId'])
			#获取LbsIp组
			LbsDetails = LbsInfo.objects.filter(IpsId=LbDetails['IpsId'])
			#获取Lbs组状态
			NLBHandleInfo = []
			NLBStatus = 0
			for LbsDetail in LbsDetails:
				LbsHandleInfo = {
					'LbsWeight' : LbsDetail['LbsWeight'],
					'LbsIp' : LbsDetail['LbsIp'],
				}
				#获取相对主备ip
				LBOperateOut = NcloudLib.HttpRequest({'action':'NLBStatus'},LbsDetail['LbsIp'],35796)
				
				NLBStatus = int(LBOperateOut['code'])
				
				NLBHandleInfo.append(LbsHandleInfo)
			if NLBStatus == 0:
				for LbsDetail in LbsDetails:
					LbsIp = LbsDetail.LbsIp
					BackendOperateOut = NcloudLib.HttpRequest(operateinfo,LbsIp,35796)
					print BackendOperateOut
					if BackendOperateOut['code'] == 0:
						BackendStatus = 1
					else:
						BackendStatus = 0
				if BackendStatus == 1:
					BackendDetails.BackendStatus = 0
					BackendDetails.save()
					code = 0
					msg = '操作成功。'
				else:
				
					code = 0
					msg = '操作失败'
		else:
			code = 1
			msg = '当前后端服务器不存在'
		'''
		except:
			code = 10001
			msg = '当前后端服务器不存在'
		'''
		return_data = {
			'code' : code,
			'msg' : msg,
		}
		return_data = json.dumps(return_data)
		return return_data
	def ActivatedBankend(self):
		#根据条件查询列表 存在继续执行 不存在返回结果
		try:
		
			BackendDetails = BackendInfo.objects.get(id=self.params['BackendId'])
			ServerBackend = '#server %s:%s weight=%s;' % (BackendDetails['RouterEips'],BackendDetails['BackendPort'],BackendDetails['BackendWeight'])
			LbMonitorDetail = LbMonitorInfo.objects.get(id=BackendDetails['LbMonitorId'])
			UpstreamName = LbMonitorDetail['LbDomain'].replace('.','')
			operateinfo = {
				'action':'ActivatedBankend',
				'parame':{
					'FileName':UpstreamName+str(LbMonitorDetail['LbPort']),
					'ServerBackend':ServerBackend,
				},
			}
			if BackendDetails:
				#获取LbsGroupId
				LbDetails = LbInfo.objects.get(LbId=BackendDetails['LbId'])
				#获取LbsIp组
				LbsDetails = LbsInfo.objects.filter(IpsId=LbDetails['IpsId'])
				#获取Lbs组状态
				NLBHandleInfo = []
				NLBStatus = 0
				for LbsDetail in LbsDetails:
					LbsHandleInfo = {
						'LbsWeight' : LbsDetail['LbsWeight'],
						'LbsIp' : LbsDetail['LbsIp'],
					}
					#获取相对主备ip
					LBOperateOut = NcloudLib.HttpRequest({'action':'NLBStatus'},LbsDetail['LbsIp'],35796)
					
					NLBStatus = int(LBOperateOut['code'])
					
					NLBHandleInfo.append(LbsHandleInfo)
				if NLBStatus == 0:
					for LbsDetail in LbsDetails:
						LbsIp = LbsDetail.LbsIp
						BackendOperateOut = NcloudLib.HttpRequest(operateinfo,LbsDetail['LbsIp'],35796)
						print BackendOperateOut
						if BackendOperateOut['code'] == 0:
							BackendStatus = 1
						else:
							BackendStatus = 0
					if BackendStatus == 1:
						BackendDetails.BackendStatus = 1
						BackendDetails.save()
						code = 0
						msg = '操作成功。'
					else:
					
						code = 0
						msg = '操作失败'
			else:
				code = 1012
				msg = '当前后端服务器不存在'
		except:
			code = 1011
			msg = '当前后端服务器不存在'
		return_data = {
			'code' : code,
			'msg' : msg,
		}
		return_data = json.dumps(return_data)
		return return_data

	def DeleteBankend(self):
		#根据条件查询列表 存在继续执行 不存在返回结果
		try:
			BackendDetails = BackendInfo.objects.get(id=self.params['BackendId'])
			if BackendDetails['BackendStatus'] == 1:
				ServerBackend = 'server %s:%s weight=%s;' % (BackendDetails['BackendIp'],BackendDetails['BackendPort'],BackendDetails['BackendWeight'])
			else:
				ServerBackend = '#server %s:%s weight=%s;' % (BackendDetails['BackendIp'],BackendDetails['BackendPort'],BackendDetails['BackendWeight'])
			BackendDetail = BackendInfo.objects.filter(LbMonitorId=BackendDetails['LbMonitorId'])
			BackendNum = len(BackendDetail)
			LbMonitorDetail = LbMonitorInfo.objects.get(id=BackendDetails['LbMonitorId'])
			UpstreamName = LbMonitorDetail['LbDomain'].replace('.','')
			operateinfo = {
				'action':'DeleteBankend',
				'parame':{
					'FileName':UpstreamName+str(LbMonitorDetail['LbPort']),
					'ServerBackend':ServerBackend,
					"BackendNum":BackendNum,
				},
			}
			if BackendDetails:
				#获取LbsGroupId
				LbDetails = LbInfo.objects.get(LbId=BackendDetails['LbId'])
				#获取LbsIp组
				LbsDetails = LbsInfo.objects.filter(IpsId=LbDetails['IpsId'])
				#获取Lbs组状态
				NLBHandleInfo = []
				NLBStatus = 0
				for LbsDetail in LbsDetails:
					LbsHandleInfo = {
						'LbsWeight' : LbsDetail['LbsWeight'],
						'LbsIp' : LbsDetail['LbsIp'],
					}
					#获取相对主备ip
					LBOperateOut = NcloudLib.HttpRequest({'action':'NLBStatus'},LbsDetail['LbsIp'],35796)
					
					NLBStatus = int(LBOperateOut['code'])
					
					NLBHandleInfo.append(LbsHandleInfo)
				if NLBStatus == 0:
					for LbsDetail in LbsDetails:
						LbsIp = LbsDetail.LbsIp
						BackendOperateOut = NcloudLib.HttpRequest(operateinfo,LbsDetail['LbsIp'],35796)
						print BackendOperateOut
						if BackendOperateOut['code'] == 0:
							BackendStatus = 1
						else:
							BackendStatus = 0
					if BackendStatus == 1:
						BackendDetails.delete()
						code = 0
						msg = '操作成功。'
					else:
					
						code = 0
						msg = '操作失败'
			else:
				code = 1012
				msg = '当前后端服务器不存在'
		except:
			code = 1011
			msg = '当前后端服务器不存在'
		return_data = {
			'code' : code,
			'msg' : msg,
		}
		return_data = json.dumps(return_data)
		return return_data