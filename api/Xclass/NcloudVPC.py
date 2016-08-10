# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os,time,uuid
#导出数据结构模块
from api.models import *

from lib import NcloudLib
from api.ManagerEch import *
#导入hashlib模块
import hashlib
#操作HandleNlb类
class HandleVPC:

	def __init__(self, Data,params):
		self.params = params
		self.Data = Data
	def DescribeVpcInfo(self):
		VpcDetails = VpcInfo.objects.filter(Zone=self.Data['Zone']).filter(UserId=self.Data['UserId'])
		if VpcDetails:
			VpcList = []
			for VpcDetail in VpcDetails:
				VpcId = VpcDetail.VpcId
				VpcName = VpcDetail.VpcName
				
				VpcSecInfo = {
					"vpcid":VpcId,
					"vpcname":VpcName,
					"VpcswList": [],
				}
				
				VpcSwitchDetails = VpcSwitch.objects.filter(VpcId=VpcId).filter(Zone=self.Data['Zone']).filter(UserId=self.Data['UserId'])
				for VpcSwitchDetail in VpcSwitchDetails:
					VswId = VpcSwitchDetail.VswId
					VswName = VpcSwitchDetail.VswName
					VswInfo = {
						"vswid":VswId,
						"vswname":VswName,
					}
					VpcSecInfo['VpcswList'].append(VswInfo)
				
				VpcList.append(VpcSecInfo)
			return_data={
				"code":0,
				"VpcList":VpcList,
				
			}
		else:
			return_data = {
				"code":100001,
				"msg":"",
			}
		return return_data
	def GainVpcInfo(self):
		VpcDetails = VpcInfo.objects.filter(VpcId=self.params['vpcid']).filter(UserId=self.Data['UserId'])
		if VpcDetails:
			for VpcDetail in VpcDetails:
				VpcId=VpcDetail.VpcId
				VpcSubnets=VpcDetail.Subnets
			return_data={
				"code":0,
				"vpcid":VpcId,
				"vpcsubnets":VpcSubnets,
				
			}
		else:
			return_data = {
				"code":100001,
				"msg":"请提交正确的专用网络ID",
			}
		return return_data
	def CreateVPC(self):
		#创建VPC Create Network
		#获取数据库最后一条
		VpcDetail = VpcInfo.objects.filter(UserId=self.Data['UserId'])
		if len(VpcDetail) ==0:
			VpcId= 'vpc-%s' % str(uuid.uuid1())[:8]
			VpcLish = VpcInfo.objects.all().order_by('-CreateTime')[0:1]
			if VpcLish:
				for VpcDetails in VpcLish:
					VpcRawId = VpcDetails.SegmentationId
				SegmentationId=VpcRawId+1
			else:
				SegmentationId=1
			#根据当前time.time()生成md5
			TenantId = NcloudLib.md5Encrypt(str(time.time()))
			
			
			Status = self.__CreateRouter(VpcId,TenantId)
			if Status['code'] == 0:
				print Status
				inVpc = VpcInfo(VpcId=VpcId,VpcName=self.params['vpcname'],NetworkType='vlan',SegmentationId=SegmentationId,Shared='False',Status='ACTIVE',Subnets=self.params['vpcsegmentation'],TenantId=TenantId,VpcBewrite='-',Zone=self.Data['Zone'],UserId=self.Data['UserId'])
				inVpc.save()
				return_data = {
					"code":0,
					"msg" :"恭喜您，创建专有网络成功",
				}
			else:
				return_data = {
					"code":0,
					"msg" :"创建专有网络失败.",
				}
		else:
			return_data = {
				"code":0,
				"msg" :"创建专有网络失败,用户名下的 VPC 数量达到配额上限.",
			}
		return return_data
	def __CreateRouter(self,VpcId,TenantId):
		#生成UUID
		#print '-------------------------------------'
		#VrtId = 'vrt-' % str(uuid.uuid1())[:8]
		Qrouter = 'qrouter-%s' % str(uuid.uuid1())
		#Qrouter = 'qrouter-' % str(uuid.uuid1())[:8]
		QrUUID = str(uuid.uuid1())
		#QrUUID = 'qr-%s' % str(uuid.uuid1())[:11]
		QRMac = NcloudLib.buildMac()
		QgUUID = str(uuid.uuid1())
		#QgUUID = 'qg-%s' % str(uuid.uuid1())[:11]
		QGMac = NcloudLib.buildMac()
		#print '-------------------------------------'
		#RouterEips = StringField(max_length=50)
		#RouterEipsId = StringField(max_length=50)
		VpcIpList = VpcIpInfo.objects.filter(IpArea=self.Data['Zone']).filter(Status=0)[0:1]
		for VpcIpDetails in VpcIpList:
			RouterEips = VpcIpDetails.IpAddress
			EipsNetMask = VpcIpDetails.NetMask
			RouterEipsId = str(VpcIpDetails.id)
			EipsGateWay = VpcIpDetails.GateWay
			VpcIpDetails.Status = 1
		operateinfo = {
			'action':'Create_Router',
			'parame':{
				'Qrouter':Qrouter,
				'QrUUID':QrUUID,
				'QRMac':QRMac,
				'QgUUID':QgUUID,
				'QGMac':QGMac,
				'RouterEips':RouterEips,
				'EipsNetMask':EipsNetMask,
				'EipsGateWay':EipsGateWay,
			},
		}
		Status = NcloudLib.HttpRequest(operateinfo,'127.0.0.1',35796)
		#print Status
		if Status['code'] == 0:
			#print 'ssaaaaaaaaaaaaa'
			#network 执行成功 插入数据

	
			VrtId = 'vrt-%s' % str(uuid.uuid1())[:8]
			VpcRouterInt=VpcRouter(VrtId=VrtId,VrtName='-',Status='ACTIVE',VpcId=VpcId,TenantId=TenantId,Zone=self.Data['Zone'],Qrouter=Qrouter,QrUUID=QrUUID,QRMac=QRMac,QgUUID=QgUUID,QGMac=QGMac,RouterEips=RouterEips,RouterEipsId=RouterEipsId,UserId=self.Data['UserId'])
			
			VtbId = 'vtb-%s' % str(uuid.uuid1())[:8]
			TargetSubnets = '11.11.0.0/20'

			VpcRouterTableInt = VpcRouterTable(VtbId=VtbId,Status='ACTIVE',TargetSubnets=TargetSubnets,NextHop='-',NextHopType = '-',Type=0,VpcId=VpcId,TenantId=TenantId,VrtId=VrtId,Zone=self.Data['Zone'],UserId=self.Data['UserId'])
			
			VpcRouterInt.save()
			VpcRouterTableInt.save()
			VpcIpDetails.save()
			return_data = {
				"code":0,
			}
		else:
			return_data = {
				"coed":1,
			}
		return return_data
	def CreateSwitch(self):
		print self.params
		if self.__verifySubnets()['code'] == 0:
			RouterDetail = VpcRouter.objects.get(VpcId=self.params['vpcid'])
			Qrouter = RouterDetail['Qrouter']
			QrUUID = RouterDetail['QrUUID']
			TenantId = RouterDetail['TenantId']
			RouterEips = RouterDetail['RouterEips']
			VpcDetail = VpcInfo.objects.get(TenantId=TenantId)
			
			SegmentationId = VpcDetail['SegmentationId']
			Tags = SegmentationId
			TunId = hex(SegmentationId) 
			VswId = 'vsw-%s' % str(uuid.uuid1())[:8]
			VswName = self.params['switchname']
			Qdhcp = 'qdhcp-%s' % str(uuid.uuid1())
			TapUUID = str(uuid.uuid1())
			TapMac = NcloudLib.buildMac()
			Cidr= self.params['subnets']
			UsableIp = pow(2,(32-int(self.params['subnets'].split('/')[1]))) - 4
			
			GatewayIp ="%s.%s.%s.1" % (self.params['subnets'].split('/')[0].split('.')[0],self.params['subnets'].split('/')[0].split('.')[1],self.params['subnets'].split('/')[0].split('.')[2])
			DnsmasqxIp = "%s.%s.%s.2" % (self.params['subnets'].split('/')[0].split('.')[0],self.params['subnets'].split('/')[0].split('.')[1],self.params['subnets'].split('/')[0].split('.')[2])
			DhcpStartIp = "%s.%s.%s.3" % (self.params['subnets'].split('/')[0].split('.')[0],self.params['subnets'].split('/')[0].split('.')[1],self.params['subnets'].split('/')[0].split('.')[2])
			Mask = self.params['subnets'].split('/')[1]
			if self.params['switchdescribe']=='':
				SwitchDescribe = '-'
			else:
				SwitchDescribe=self.params['switchdescribe']
			operateinfo = {
				'action':'Create_Switch',
				'parame':{
					'Qdhcp':Qdhcp,
					'TapUUID':TapUUID,
					'TapMac':TapMac,
					'Mask' : Mask,
					'GatewayIp':GatewayIp,
					'DnsmasqxIp':DnsmasqxIp,
					'Qrouter':Qrouter,
					'QrUUID':QrUUID,
					'Tags':Tags,
					'TunId':TunId,
					'Cidr':Cidr,
					'RouterEips':RouterEips,
					'DhcpStartIp':DhcpStartIp,
					'UsableIp':UsableIp,
				},
			}
			Status = NcloudLib.HttpRequest(operateinfo,'127.0.0.1',35796)
			if Status['code'] == 0:
				operateinfos = {
				'action':'Create_TunFlow',
				'parame':{
					'Tags':Tags,
					'TunId':TunId,
				},
			}
				KvmList = KvmInfo.objects.filter(KVMArea=self.Data['Zone'])
				KvmTunStatus = 1
				for KvmDetails in KvmList:
					Status = NcloudLib.HttpRequest(operateinfos,KvmDetails.KVMIp,35796)
					
					if Status['code'] == 0:
						KvmTunStatus = 0
					else:
						KvmTunStatus = 1
						break
				if KvmTunStatus == 0:
					intSwitch = VpcSwitch(VswId=VswId,VswName=VswName,Status='ACTIVE',VpcId=self.params['vpcid'],TenantId=TenantId,Qdhcp=Qdhcp,TapUUID=TapUUID,TapMac=TapMac,Cidr=Cidr,GatewayIp=GatewayIp,DnsmasqxIp=DnsmasqxIp,UsableIp=UsableIp,SwitchDescribe=SwitchDescribe,Zone=self.Data['Zone'],UserId=self.Data['UserId'])
					intSwitch.save()
					return_data = {
						"code": 0,
						"msg":"创建交换机成功。",
					}
				else:
					return_data = {
						"code": 100013,
						"msg":"创建交换机失败。",
					}
			else:
				return_data = {
					"code": 100013,
					"msg":"创建交换机失败。",
				}
		else:
			return_data = {
				"code": 10012,
				"msg":"对不起，您输入的网段不正确。"
			}
		return return_data
	def __verifySubnets(self):
		#判断 subnets 是否合法
		#print self.params['subnets'].split("/")
		try:
			if int(self.params['subnets'].split("/")[0].split('.')[3]) == 0:
				if 0 < int(self.params['subnets'].split("/")[0].split('.')[2]) <=255:
					
					if 23 <= int(self.params['subnets'].split("/")[1]) <= 29:
						# 网段判断 self.params['subnets'].split("/")[0].split('.')
						'''
						self.params['vpcsubnets'].split("/")[0].split('.')[0]
						self.params['vpcsubnets'].split("/")[0].split('.')[1]
						self.params['subnets'].split("/")[0].split('.')[0]
						self.params['subnets'].split("/")[0].split('.')[1]
						'''
						if self.params['vpcsubnets'].split("/")[0].split('.')[0] == self.params['subnets'].split("/")[0].split('.')[0] and self.params['vpcsubnets'].split("/")[0].split('.')[1] == self.params['subnets'].split("/")[0].split('.')[1]:
							
							#print self.params['subnets'].split("/")[0].split('.')
							return_data = {
								"code" :0,
								"msg" : "网段正确",
							}
						else:
							return_data = {
								"code": 10012,
								"msg":"您输入的网段不正确"
							}
				elif int(self.params['subnets'].split("/")[0].split('.')[2]) == 0:
					if 16 <= int(self.params['subnets'].split("/")[1]) <= 29:
						if self.params['vpcsubnets'].split("/")[0].split('.')[0] == self.params['subnets'].split("/")[0].split('.')[0] and self.params['vpcsubnets'].split("/")[0].split('.')[1] == self.params['subnets'].split("/")[0].split('.')[1]:
							return_data = {
								"code": 0,
								"msg":"网段正确"
							}
				else:
					return_data = {
						"code": 1,
						"msg":"子网不在16-29之间"
					}
			else:
				return_data = {
					"code": 1,
					"msg":"最后地址段不为0"
				}
			
			
		except:
			return_data = {
					"code": 1,
					"msg":"最后地址段不为0"
			}
		return return_data
	def AddEchToSwitch(self):
		#判断 提交的switch 是否存在
		try:
			VpcSwDetails = VpcSwitch.objects.get(VswId=self.params['vswid'])
			VpcDetails = VpcInfo.objects.get(TenantId=VpcSwDetails['TenantId'])
			EchDetails = EchInfo.objects.get(EchId=self.params['echid'])
			EchMacs=EchDetails['EchMacs']
			EchName=EchDetails['EchName']
			EchKvmIp = EchDetails['EchVncIp']
			TapUUID = EchDetails['TapUUID']
			Tags = VpcDetails['SegmentationId']
			DnsmasqxIp = VpcSwDetails['DnsmasqxIp']
			UsableIp = VpcSwDetails['UsableIp']
			Qdhcp = VpcSwDetails['Qdhcp']
			operateinfo = {
				'action':'AddEchToSwitch',
				'parame':{
					'EchMacs':EchMacs,
					'Qdhcp':Qdhcp,
					'DnsmasqxIp':DnsmasqxIp,
					'UsableIp':UsableIp,
					'EchName':EchName,
					'Type':1,
				},
			}
			Status = NcloudLib.HttpRequest(operateinfo,'127.0.0.1',35796)
			if Status['code'] == 0:
				EchIp = Status['EchIp']
				operateinfos = {
					'action':'SetEchTapTags',
					'parame':{
						'Tags':Tags,
						'TapUUID':TapUUID,
						
					},
				}
				#Status = NcloudLib.HttpRequest(operateinfos,EchKvmIp,35796)
				
				Status = {
					'code': 0,
					}
				if Status['code'] == 0:
					EchDetails.EchIp = EchIp
					EchDetails.TenantId = VpcSwDetails['TenantId']
					EchDetails.VlanId = Tags
					EchDetails.save()
					return_data = {
						"code":0,
						"msg": '成功将云主机添加到当前交换机。',
					}
				else:
					return_data = {
							"code": 1,
							"msg":"对不起，无法将云主机添加到当前交换机。"
					}
		except:
			return_data = {
					"code": 1,
					"msg":"对不起，无法将云主机添加到当前交换机。"
			}
		return return_data
	def CreateForwardRule(self):
		'''
		#params {"action":"CreateForwardRule","forwardname":"test","serverport":"80","clientport":"80","forwardprotocol"
		#:"tcp","echid":"instances-227a3fe6","vrtid":"vrt-f7542f4e"}
		
		
		'''
		#根据 echid 查询 Ip 地址
		#验证同一个外网ip服务端口是否被转发存在则 返回失败，
		ForwardRuleDetails = VpcForwardRule.objects.filter(ServerPort=self.params['serverport']).filter(Zone=self.Data['Zone']).filter(UserId=self.Data['UserId'])
		if not ForwardRuleDetails:
			
			RouterDetails = VpcRouter.objects.get(VrtId=self.params['vrtid'])
			RouterEips = RouterDetails.RouterEips
			Qrouter = RouterDetails.Qrouter
			TenantId = RouterDetails.TenantId
			EchDetails = EchInfo.objects.get(EchId=self.params['echid'])
			EchIp = EchDetails.EchIp
			operateinfo = {
				'action':'CreateForwardRule',
				'parame':{
					'RouterEips':RouterEips,
					'ForwardProtocol':self.params['forwardprotocol'],
					'ServerPort':self.params['serverport'],
					'EchIp':EchIp,
					'Clientport':self.params['clientport'],
					'Qrouter':Qrouter,
				},
			}
			Status = NcloudLib.HttpRequest(operateinfo,'127.0.0.1',35796)
			#ip netns exec qroute iptables -t nat -I PREROUTING --dst RouterEips -p forwardprotocol --dport serverport -j DNAT --to-destination EchIp:clientport
			if Status['code'] == 0:
				#将数据插入数据库
				VpcForwardRuleint = VpcForwardRule(ForwardName=self.params['forwardname'],ServerPort=self.params['serverport'],Clientport=self.params['clientport'],EchId=self.params['echid'],VrtId=self.params['vrtid'],RouterEips=RouterEips,EchIp=EchIp,ForwardProtocol=self.params['forwardprotocol'],Status='ACTIVE',TenantId=TenantId,Zone=self.Data['Zone'],UserId=self.Data['UserId'])
				VpcForwardRuleint.save()
				return_data = {
					"code" : 0,
					"msg":"成功创建端口转发规则。",
				}
			else:
				return_data = {
					"code":10202,
					"msg" : "对不起，无法为您创建端口转发规则。",
				}
		else:
			return_data = {
				"code":10201,
				"msg" : "对不起，无法为您创建端口转发规则。",
			}
		return return_data