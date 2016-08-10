# coding=utf-8

#导入常用模块
import datetime,json,md5,sys,os,time
#导入数据结构模块
from api.models import *

from lib import NcloudNlbLib
from lib import NcloudLib
from api.ManagerEch import *
#导入hashlib模块
import hashlib
#操作HandleNlb类
class HandleNlb:

	def __init__(self, Data,params):
		self.params = params
		self.Data = Data
	def CreateLBMonitor(self):
		#验证白名单地址格式是否正常 正确输入 1
		HandleVisitPower = NcloudNlbLib.HandleVisitPlace(self.params)
		if HandleVisitPower['VisitPlaceFruit'] == 1:
			#提交域名地址
			Domain = self.params['listeners'][0]['loadbalancer_listener_name']
			LinstenDomain= LbMonitorInfo.objects.filter(LbDomain=Domain)
			#提交负载端口
			listener_port = self.params['listeners'][0]['listener_port']
			#判断当前提交的域名是否已存在
			if LinstenDomain:
				#存在域名判断端口 存在则域名端口存在 返回结果 否则域名域名端口不存在可创建
				ListenPort = LbMonitorInfo.objects.filter(LbDomain=Domain).filter(LbPort=listener_port)
				if ListenPort:
					#请重新输入域名或端口
					code = 1
					msg = '请重新输入域名或端口'
				else:
					#端口不存在创建
					code = 1
					msg = '端口不存在创建'
			else:
				#不存在域名创建
				LbList = LbInfo.objects.get(LbId=self.params['loadbalancerid'])
				EipList = EipInfo.objects.get(id=LbList.EipId)
				EipGroup = EipList.EipGroup
				DomainName = Domain.split('.')[len(Domain.split('.'))-2]
				UpstreamName = Domain.replace('.','')
				
				#判断轮询类型
				balance_mode = self.params['listeners'][0]['balance_mode']
				if balance_mode == 'roundrobin':
					balance_mode = ''
				else:
					balance_mode = 'ip_hash;'
				#判断session类型
				session_sticky = self.params['listeners'][0]['session_sticky']
				if session_sticky:
					session_sticky = 'session_sticky;'
				else:
					session_sticky = ''
				#判断检测类型
				
				healthy_check_method = self.params['listeners'][0]['healthy_check_method']
				checkinterval = self.params['listeners'][0]['healthy_check_option'].split('|')[0]
				checktimeout = self.params['listeners'][0]['healthy_check_option'].split('|')[1]
				checkfall = self.params['listeners'][0]['healthy_check_option'].split('|')[2]
				checkrise = self.params['listeners'][0]['healthy_check_option'].split('|')[3]
				forwardfor = self.params['listeners'][0]['forwardfor'].split('|')
				listener_option = self.params['listeners'][0]['listener_option'].split('|')
				checkinterval = int(checkinterval) * 1000
				checktimeout = int(checktimeout) * 1000

				if healthy_check_method == 'tcp':
					check = 'check interval=%s rise=%s fall=%s timeout=%s type=tcp;' % (checkinterval,checkrise,checkfall,checktimeout)
					check_http_send = ''
					check_http_expect_alive = 'check_http_expect_alive http_2xx http_3xx http_4xx;'
				else:
					check = 'check interval=%s rise=%s fall=%s timeout=%s type=http;' % (checkinterval,checkrise,checkfall,checktimeout)
					check_http_send = 'check_http_send "GET %s HTTP/1.0\r\n\r\n";'
					check_http_expect_alive = 'check_http_expect_alive http_2xx http_3xx http_4xx;'
				#判断是否显示客户端
				if forwardfor[0] == '1':
					ClientIP = "proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;"
				else:
					ClientIP=''
				if forwardfor[1] == '1':
					LBID = "proxy_set_header QC-LB-ID $server_name;"
				else:
					LBID = ''
				if forwardfor[2] == '1':
					LBIP = "proxy_set_header QC-LB-IP $server_addr;"
				else:
					LBIP = ''
				if forwardfor[3] == '1':
					ClientProto = "proxy_set_header X-Forwarded-Proto http;"
				else:
					ClientProto = ''
				
				if listener_option[1] == '1':
					RealIP= """
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $remote_addr;"""
				else:
					RealIP = ''
				if listener_option[2] == '1':
					gzip = 'gzip on;'
				else:
					gzip = ''
				timeout = self.params['listeners'][0]['timeout']
				connecttimeout = """
							proxy_connect_timeout %s;
							proxy_read_timeout %s;
							proxy_send_timeout %s;
				""" % (timeout,timeout,timeout)
				Upstream = {
					"UpstreamName":UpstreamName,
					"check":check,
					"check_http_send":check_http_send,
					"check_http_expect_alive":check_http_expect_alive,
					"session":session_sticky,
				}
				if self.params['listeners'][0]['balance_mode'] == 'roundrobin':
					LbMode = 0
				LbsList = LbsInfo.objects.filter(LbsZone=self.Data['Zone']).filter(IpsId=LbList.IpsId)
				if LbsList:
					#获取负载集群状态
					NLBHandleInfo = []
					NLBStatus = 0
					#通过LbInfo中LbsId 查询LbsInfo中LbsWeight 
					
					#LbsWeightDetail = LbsInfo.objects.get(id=LbList.LbsId)
					
					for LbsDetail in LbsList:
						LbsHandleInfo = {
							'LbsIp' : LbsDetail['LbsIp'],
							'LbsWeight' : LbsDetail['LbsWeight'],
							'id' : str(LbsDetail['id']),
							'EchIp' : LbsDetail['EchIp'],
						}
						#获取相对主备ip
						LBOperateOut = NcloudLib.HttpRequest({'action':'NLBStatus'},LbsDetail['LbsIp'],35796)
						
						NLBStatus = int(LBOperateOut['code'])
						
						NLBHandleInfo.append(LbsHandleInfo)
					#如果用户类型不等于3则判断当前LB下是否存在同IP，同端口 如果存在不执行LVS添加Real 如不存在需添加LVS Real配置

					print NLBHandleInfo

					LbIp = LbList.LbIp
					Tip = LbIp.split(',')[0]
					Uip = LbIp.split(',')[1]
                    
					for NLBHandle in NLBHandleInfo:
						
						server = """
server {
	listen %s:%s;
	server_name %s;
	location / {
		include server/%s/*.conf;
	}
}""" % (NLBHandle['EchIp'],listener_port,Domain,UpstreamName+listener_port)


						if NLBHandle['LbsWeight'] == 1:
							ServerMASTER = server
						else:
							ServerBACKUP = server
					if self.Data['UserType'] != 3:
						#获取Eip地址
						LbMonitorList = LbMonitorInfo.objects.filter(LbId=self.params['loadbalancerid']).filter(LbPort=listener_port)
						if LbMonitorList:
							CreateLVSVirtualStatus = 1
							pass
						else:
							#获取Eips
							#LBDetails = LbInfo.objects.get(LbId=self.params['loadbalancerid'])
							#EipDetails = EipInfo.objects.get(AssignId=LBDetails['LbId'])
							RealIps = []
							for LbsDetails in NLBHandleInfo:
								RealIps.append(LbsDetails['EchIp'])
							#获取状态
							LvsList = LvsInfo.objects.filter(GroupId=LbList.LvsGroupId)
							if LvsList:
								LVSHandleInfo = []
								LVSStatus = 0
								for LvsDetail in LvsList:
									LvsHandle = {
										'LvsIp' : LvsDetail['LvsIp'],
									}
									#获取相对主备ip NcloudLib.HttpRequest({'action':'NLBStatus'},LbsDetail['LbsIp'],35796)
									#获取LVS状态
									LVSOperateOut = NcloudLib.HttpRequest({'action':'LVSStatus'},LvsDetail['LvsIp'],35796)
									
									LVSStatus = int(LVSOperateOut['code'])
									
									LVSHandleInfo.append(LvsHandle)
								if LVSStatus == 0:
									#获取LVS Real Info
									parame = {
										'Tip' : Tip,
										'Uip' :Uip,
										'listener_port' : listener_port,
										'RealIps' : RealIps,
									}
									LvsVirtualInfo = NcloudNlbLib.GetDoubletLvsVirtualCfg(parame)
									Lvsoperateinfo = {
										'action' : 'CreateLVSVirtual',
										'parame' : {
											'LvsVirtualInfo' : LvsVirtualInfo['LVSVirtualInfo'],
											'VirtualFileName' : LbIp+'.'+listener_port,
											'Eips' : [Tip,Uip],
											'listener_port' : listener_port,
										},
									}
									print Lvsoperateinfo
									for LvsHandles in LVSHandleInfo:
										LVSOperateOut = NcloudLib.HttpRequest(Lvsoperateinfo,LvsHandles['LvsIp'],35796)
										if LVSOperateOut['code'] == 0:
											CreateLVSVirtualStatus = 1
										else:
											CreateLVSVirtualStatus = 0
					else:
						CreateLVSVirtualStatus = 1
					if NLBStatus == 0:
						proxy_pass = 'proxy_pass http://%s;' % UpstreamName
						servers = {
							"proxy_pass":proxy_pass,
							"ClientIP":ClientIP,
							"LBID":LBID,
							"LBIP":LBIP,
							"ClientProto":ClientProto,
							"RealIP":RealIP,
							"gzip":gzip,
							"connecttimeout":connecttimeout,
							"VisitPlaceList" : HandleVisitPower['VisitPlaceList'],
						}
						for LbsDetail in LbsList:
							if LbsDetail['LbsWeight'] == 1:
								Lbsoperateinfo = {
									'action':'CreateLBMonitor',
									'parame':{
										'Upstream':Upstream,
										'server':ServerMASTER,
										'servers':servers,
										'FileName':UpstreamName+listener_port,
									},
								}
							else:
								Lbsoperateinfo = {
									'action':'CreateLBMonitor',
									'parame':{
										'Upstream':Upstream,
										'server':ServerBACKUP,
										'servers':servers,
										'FileName':UpstreamName+listener_port,
									},
								}
							LbsId = LbsDetail.id
							LbsIp = LbsDetail.LbsIp
							LbsZone = LbsDetail.LbsZone
							LBOperateOut = NcloudLib.HttpRequest(Lbsoperateinfo,LbsIp,35796)
							print LBOperateOut
							if LBOperateOut['code'] == 0:
								CreateLBMonitorStatus = 1
							else:
								CreateLBMonitorStatus = 0
						if CreateLBMonitorStatus == 1 and CreateLVSVirtualStatus == 1:
							inLbMonitor = LbMonitorInfo(LbDomain=Domain,LbProtocol=self.params['listeners'][0]['listener_protocol'],LbPort=listener_port,LbMode=LbMode,SessionSticky=self.params['listeners'][0]['session_sticky'],HealthyCheckMethod=self.params['listeners'][0]['healthy_check_method'],HealthyCheckOption=self.params['listeners'][0]['healthy_check_option'],Forwardfor=self.params['listeners'][0]['forwardfor'],Timeout=timeout,LbOption=self.params['listeners'][0]['listener_option'],LbId=self.params['loadbalancerid'])
							inLbMonitor.save()
							#print LBOperateOut
							code = 0
							msg = '创建成功，您添加域名解析就可以通过域名访问了哦。'
						else:
							code = 1
							msg = '添加监听器失败,请联系客服'

					else:
						code = 1
						msg = '当前负载集群中有一个或多个存在故障，等待恢复后再重新操作。'
				else:
					code = 1
					msg = '负载集群不存在,请联系客服'
		else:
			code = 1
			msg = '您输入的白名单有问题，请您确认是否存在错误。'
		return_data = {
			'code' : code,
			'msg' : msg,
		}
		return_data = json.dumps(return_data)
		return return_data
	def DeleteLBMonitor(self):
		#查询 LbMonitorInfo 获取 LbId
		LbMonitorDetails = LbMonitorInfo.objects.get(id=self.params['Lbmonitorid'])
		#查询 LbInfo 根据 LbId 获取 LbsGroupId
		LbDetails = LbInfo.objects.get(LbId=LbMonitorDetails['LbId'])
		LbsList = LbsInfo.objects.filter(LbsZone=self.Data['Zone']).filter(GroupId=LbDetails.LbsGroupId)
		if LbsList:
			#获取负载集群状态
			NLBHandleInfo = []
			NLBStatus = 0
			for LbsDetail in LbsList:
				LbsHandleInfo = {
					'LbsWeight' : LbsDetail['LbsWeight'],
					'LbsIp' : LbsDetail['LbsIp'],
					'id' : str(LbsDetail['id']),
				}
				#获取相对主备ip
				LBOperateOut = Operate(LbsDetail['LbsIp'],{'action':'NLBStatus'})
				
				NLBStatus = int(LBOperateOut)
				
				NLBHandleInfo.append(LbsHandleInfo)
			#获取当前 LbId 下 LbMonitor 同端口数量 如果为1 则需删除 如果用户类型为3则跳过
			if self.Data['UserType'] != 3:
			
				LbMonitorList = LbMonitorInfo.objects.filter(LbId=LbMonitorDetails['LbId']).filter(LbPort=LbMonitorDetails['LbPort'])
				if len(LbMonitorList) != 1:
					CreateLVSVirtualStatus = 1
				else:
					LvsList = LvsInfo.objects.filter(GroupId=LbDetails.LvsGroupId)
					if LvsList:
						LVSHandleInfo = []
						LVSStatus = 0
						for LvsDetail in LvsList:
							LvsHandle = {
								'LvsIp' : LvsDetail['LvsIp'],
							}
							#获取相对主备ip
							LVSOperateOut = Operate(LvsDetail['LvsIp'],{'action':'LVSStatus'})
							
							LVSStatus = int(LVSOperateOut)
							
							LVSHandleInfo.append(LvsHandle)
						if LVSStatus == 0:

							Lvsoperateinfo = {
								'action' : 'DeleteLVSVirtual',
								'parame' : {
									'VirtualFileName' : LbDetails['LbIp']+'.'+str(LbMonitorDetails['LbPort']),
								},
							}
							print Lvsoperateinfo
							for LvsHandles in LVSHandleInfo:
								LVSOperateOut = Operate(LvsHandles['LvsIp'],Lvsoperateinfo)
								if LVSOperateOut == 'done':
									CreateLVSVirtualStatus = 1
								else:
									CreateLVSVirtualStatus = 0
			else:
				CreateLVSVirtualStatus = 1
			UpstreamName = LbMonitorDetails['LbDomain'].replace('.','')
			Lbsoperateinfo = {
				'action':'DeleteLBMonitor',
				'parame':{
					'FileName':UpstreamName+str(LbMonitorDetails['LbPort']),
				},
			}
			if NLBStatus == 0:
				for LbsDetail in LbsList:
					LbsIp = LbsDetail.LbsIp
					LBOperateOut = Operate(LbsIp,Lbsoperateinfo)
					print LBOperateOut
					if LBOperateOut == 'done':
						CreateLBMonitorStatus = 1
					else:
						CreateLBMonitorStatus = 0
				if CreateLBMonitorStatus == 1 and CreateLVSVirtualStatus == 1:
					#删除 LbMonitorInfo BackendInfo
					LbMonitorDetails.delete()
					BackendList = BackendInfo.objects.filter(LbMonitorId=str(LbMonitorDetails['id']))
					BackendList.delete()
					code = 0
					msg = '删除完成。'
				else:
					code = 1
					msg = '添加监听器失败,请联系客服'

			else:
				code = 1
				msg = '当前负载集群中有一个或多个存在故障，等待恢复后再重新操作。'
		else:
			code = 1
			msg = '负载集群不存在,请联系客服'
		return_data = {
			'code' : code,
			'msg' : msg,
		}
		return_data = json.dumps(return_data)
		return return_data