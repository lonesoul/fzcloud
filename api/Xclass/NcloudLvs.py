# coding=utf-8
'''
2015-11-06 

shengyuan


'''
#导出常用模块
import datetime,json,md5,sys,os,time,uuid
#导出数据结构模块
from api.models import *

from lib import NcloudLib
import requests

#from api.ManagerEch import *
#导入hashlib模块
import hashlib
#操作 HandleEch 类
class HandleLvs:

	def __init__(self, Data,params):
		self.params = params
		self.Data = Data
	def CreateEch(self):
		KVMList = KvmInfo.objects.filter(KVMArea=self.params['zone']).filter(KVMSurplusCpu__gte=int(self.params['cpu'])).filter(KVMSurplusMem__gte=int(self.params['memory'])).order_by('-KVMSurplusCpu')[0:1]
		if KVMList:
			for kvmDetails in KVMList:
				kvmDetail = KvmInfo.objects.get(id=kvmDetails.id)
				kvmDetail.KVMSurplusCpu = kvmDetails.KVMSurplusCpu - int(self.params['cpu'])
				kvmDetail.KVMSurplusMem = kvmDetails.KVMSurplusMem - int(self.params['memory'])
				#kvmDetail.save()
			ImageList = ImagesInfo.objects.get(ImagesId=self.params['image_id'])
			ImagesPlatform = ImageList.ImagesPlatform
			if ImagesPlatform == 'linux':
				SystemVolume = 20
			else:
				SystemVolume = 40
			#get image list
			print self.params['image_id']
			GetImageList = ImagesList.objects.filter(ImagesId=self.params['image_id']).filter(ImagesStatus=1)[0:1]
			if GetImageList:
				for imageDetails in GetImageList:
					imageDetail = ImagesList.objects.get(id=imageDetails.id)
					ImagesId = imageDetail.ImagesName
					SYSPosition = imageDetail.SYSPosition
					NetWorkId = imageDetail.NetWorkId
					DiskPosition = imageDetail.SYSPosition
					ImagesPosition = imageDetail.ImagesPosition
					PoolId = imageDetails.PoolId
					imageDetail.ImagesStatus = 0
				#生成ECH数据
				#生成EchIp 获取当前
				SwitchDetails = VpcSwitch.objects.get(VswId=self.params['vswid'])
				TenantId = SwitchDetails.TenantId
				DnsmasqxIp = SwitchDetails.DnsmasqxIp
				UsableIp = SwitchDetails.UsableIp
				Qdhcp = SwitchDetails.Qdhcp
				VpcDetails = VpcInfo.objects.get(TenantId=TenantId)
				SegmentationId = VpcDetails.SegmentationId
				NetEchNumList = EchInfo.objects.filter(TenantId=TenantId)
				NetEchNum = len(NetEchNumList)
				if NetEchNum < UsableIp:
					EchIp = '%s.%s.%s.%s' % (DnsmasqxIp.split('.')[0],DnsmasqxIp.split('.')[1],DnsmasqxIp.split('.')[2],int(DnsmasqxIp.split('.')[3])+NetEchNum+1)
				#IpList = IpInfo.objects.filter(IpArea=self.params['zone']).filter(IpType=0).filter(IpUseNum__lte=254).order_by('IpUseNum')[0:1]
				#if IpList:
					'''
					for ipDetails in IpList:
						ipDetail = IpInfo.objects.get(id=ipDetails.id)
						IpNet = ipDetail.IpAddress
						EchRawIpNum = ipDetail.IpUseNum + 1
						EchIp = '%s.%s' % (IpNet,EchRawIpNum)
						EchMask = ipDetail.NetMask
						EchGW = ipDetail.GateWay
						ipDetail.IpUseNum = EchRawIpNum
					'''
					#生成ECHUUID
					EchUUID = str(uuid.uuid1())
					#生成 tapUUID
					TapUUID = str(uuid.uuid1())
					#获取 VNC 端口 #更具端口序列插叙 最大一个 + 1
					EchLish = EchInfo.objects.filter(EchZone=self.Data['Zone']).order_by('-EchVncPort')[0:1]
					if EchLish:
						for Ech in EchLish:
							VNCPort = Ech.EchVncPort +1
					else:
						VNCPort = 59001
					#生成ECHID
					EchId = 'i-%s' % EchUUID[:8]
					#生成ECHNAME
					EchName = 'iZ%sZ' % EchId.split('-')[1]
					#生成ECHNETID
					Tap = 'tap%s' % TapUUID[:11]
					#生成MAC地址
					EchMac = NcloudLib.buildMac()
					MvEchInfo = {
						'action':'MvEchInfo',
						'parame':{
							'EchId':EchId,
							'ImagesPosition':ImagesPosition,
							'ImagesId':ImagesId,
							'EchUUID':EchUUID,
						}
					}
					DeleteEchImages = {
						'action':'DeleteEchImages',
						'parame':{
							'EchId':EchId,
							'ImagesPosition':ImagesPosition,
							'ImagesId':ImagesId,
							'EchUUID':EchUUID,
						}
					}
					operateinfo = {
						'action':'Create_ech',
						'parame':{
							'EchId':EchId,
							'EchName':EchName,
							'EchCpu':int(self.params['cpu']),
							'EchMem':int(self.params['memory']),
							'EchUUID':EchUUID,
							'TapUUID':TapUUID,
							'Tap':Tap,
							'EchVNCPort':VNCPort,
							'EchIp':EchIp,
							'EchPlatform':ImageList.ImagesPlatform,
							'ImagesId':ImagesId,
							'ImagesPosition':SYSPosition,
							'SYSPosition':SYSPosition,
							'EchMac':EchMac,
						},
					}
					#读取本地 存储list地址 如果地址为等于二 则 for  循环判断
					GfsList = GfsInfo.objects.filter(Zone=self.Data['Zone']).filter(GfsId=PoolId)
					GfsIps = ''
					GfsIpList = []
					if GfsList:
						for g in xrange(len(GfsList)):
							GfsIp = GfsList[g].GfsIp
							MvEchStatus = NcloudLib.HttpRequest(MvEchInfo,GfsIp,35796)
							if MvEchStatus['code'] == 0:
								GfsIps = GfsIp
								GfsIpList.append(GfsIps)
								#设置状态为成功 0
								
							else:
								#判断当前 g值 如果为0 则直接跳出 如果为1 则删除0中的镜像
								if g == 0:
									break
								else:
									#删除上一次移动的镜像
									MvEchStatus = NcloudLib.HttpRequest(DeleteEchImages,GfsIps,35796)
									GfsIps = ''
					
						if GfsIps != '':
							
							#创建云主机
							#print kvmDetail.KVMIp
							#发送至KVM主机创建
							Status = NcloudLib.HttpRequest(operateinfo,kvmDetail.KVMIp,35796)
							#print Status
							#如果创建成功 则生成disk磁盘数据
							if Status['code'] == 0:
								imageDetail.save()
								#生成DISKUUID =
								DiskUUID = str(uuid.uuid1())
								#DiskLish = DiskInfo.objects.all().order_by('-CreateTime')[0:1]
								'''
								#if DiskLish:
									for Disk in DiskLish:
										DiskRawId = Disk.DiskId
									DiskRawNum = DiskRawId.split('-')
									#生成EId
									DiskNum = int(DiskRawNum[1]) + 1
									#生成DiskID
									DiskId = 'd-%s' % DiskNum
									#生成DiskNAME
									DiskName = 'DZ%sZ' % DiskNum
								else:
									DiskNum = 1000001
									#生成ECHID
									DiskId = 'd-%s' % DiskNum
									#生成DiskNAME
									DiskName = 'DZ%sZ' % DiskNum
								'''
								DiskId = 'd-%s' % DiskUUID[:8]
								DiskName = 'DZ%sZ' % DiskUUID[:8]
								inDisk = DiskInfo(DiskId=DiskId,DiskName=DiskName,DiskVolume=SystemVolume,DiskZone=PoolId,DiskPosition=DiskPosition,DiskMount='vda',DiskAttr='system',EchId=EchId,UserId=self.Data['UserId'])
								inDisk.save()
								'''
								for datavposition in params['data']:
									if datavposition == '0':
										pass
									else:
										#生成存储空间ID
										diskindex = params['data'].index(datavposition)
										DiskdataId = '%s-%s' % (DiskId,diskindex)
										DiskdataName = DiskdataId.replace('-','')
										DiskdataName = DiskdataName.upper()
										DiskdataPosition = diskdata[diskindex]
										if diskindex == 0:
											DiskdataMount = 'vdb'
										elif diskindex == 1:
											DiskdataMount = 'vdc'
										elif diskindex == 2:
											DiskdataMount = 'vdd'
										elif diskindex == 3:
											DiskdataMount = 'vde'
							
										inDiskdata = DiskInfo(DiskId=DiskdataId,DiskName=DiskdataName,DiskVolume=int(datavposition),DiskZone='SHJ1',DiskPosition=DiskdataPosition,DiskMount=DiskdataMount,DiskAttr='data',EchId=EchId,UserId=str(UserVncId.id))
										inDiskdata.save()
								'''
								#获取MAC地址
								'''
								operateinfo = {'action':'ech_mac','parame':{'EchId':EchId,}}
								
								EchMacOperateOut = NcloudLib.HttpRequest(operateinfo,kvmDetail.KVMIp,35796)
								#print EchMacOperateOut
								EchMac = EchMacOperateOut['macs']
								'''
								#print EchMac
								
								inech = EchInfo(EchId=EchId,EchName=EchName,EchBewrite='',EchZone=self.params['zone'],EchCpu=int(self.params['cpu']),EchMemory=int(self.params['memory']),ImageId=self.params['image_id'],EchIp=EchIp,EchVncIp=kvmDetail.KVMIp,EchVncPort=VNCPort,EchPaymentType=0,EchPaymentDate=0,EchMacs=EchMac,TapUUID=TapUUID,EchUUID=EchUUID,TenantId=TenantId,VlanId=SegmentationId,UserId=self.Data['UserId'])
								kvmDetail.save()
								
								#d.save()
								#ipDetail.save()
								inech.save()
								UserVncId = UserInfo.objects.get(id=self.Data['UserId'])
								vncpasstoken = "%s%s%s" %(UserVncId.VNCPasswd,'NDZ',VNCPort)
								#print vncpasstoken
								vnchash = md5.new()
								vnchash.update(vncpasstoken)
								token = '%s: %s:%s\n' % (vnchash.hexdigest(),kvmDetail.KVMIp,VNCPort)
								f = open("vnc_tokens",'a')
								f.write(token)
								f.close()

								#添加MAC及IP至DHCP服务器
								#EchMac、EchIp 、EchId
								operateinfo = {
									'action':'AddEchToSwitch',
									'parame':{
										'EchName':EchName,
										'EchMacs':EchMac,
										'EchIp':EchIp,
										'Qdhcp':Qdhcp,
										'Type':0,
									}
								}
								
								HostOperateOut =  NcloudLib.HttpRequest(operateinfo,'192.168.1.186',35796)
								#print HostOperateOut
								if HostOperateOut == 'done':
									return HttpResponse('1')
								else:
									return HttpResponse('0')
								
								return_data = {
									'code':0,
									'Status': '恭喜，创建云主机成功。',
									'msg' : '恭喜，创建云主机成功。',
									'Zone':self.Data['Zone'],
								}
								#创建EHC云主机结束
							else:
								#增加存储容量 storageInfo
								for Gfsip in GfsIpList: 
									MvEchStatus = NcloudLib.HttpRequest(DeleteEchImages,Gfsip,35796)
								return_data = {
									'code':100002,
									'Status': '无法创建移动用主机镜像文件',
									'msg' : '对不起，暂时无法为您创建主机，请稍后再试，谢谢',
								}
	
	
						else:
							return_data = {
								'code':100002,
								'Status': '无法创建移动用主机镜像文件',
								'msg' : '对不起，暂时无法为您创建主机，请稍后再试，谢谢',
							}
								
						'''
						DeleteEchImages = {
							'action':'DeleteEchImages',
							'parame':{
								'EchId':EchId,
								'ImagesPosition':ImagesPosition,
							}
						}
						MvEchStatus = NcloudLib.HttpRequest(DeleteEchImages,GfsIp,35796)
						'''
						#如果成功继续 否则返回失败结果
					else:
						return_data = {
							'code':100002,
							'Status': '当前区域存储区域不能满足需求',
							'msg' : '对不起，暂时无法为您创建主机，请稍后再试，谢谢',
						}
				
				else:
					return_data = {
						'code':100002,
						'Status': '内网ip不能满足需求',
						'msg' : '对不起，暂时无法为您创建主机，请稍后再试，谢谢',
					}
			
			else:
				return_data = {
					'code':100002,
					'Status': 'system data no系统空间不足',
					'msg' : '对不起，暂时无法为您创建主机，请稍后再试，谢谢',
				}
				
		else:
			return_data = {
				'code':100002,
				'Status': 'KVM剩余CPU或MEM不足',
				'msg' : '对不起，暂时无法为您创建主机，请稍后再试，谢谢',
			}
		return return_data
	def EchStatus(self):
		EchList = LvsInfo.objects.get(EchId=self.params['EchId'])
		operateinfo = {'action':'ech_status','parame':{'EchId':self.params['EchId'],}}
		KvmOperateOut = NcloudLib.HttpRequest(operateinfo,EchList['EchVncIp'],35796)
		if KvmOperateOut['code'] == 0:
			return_data = KvmOperateOut
		else:
			return_data = {
				'code':100001,
				'Status': 'shutdown',
			}
		return return_data
	def EchStart(self):
		EchList = LvsInfo.objects.get(EchId=self.params['EchId'])
		VlanId = EchList.VlanId
		TapUUID = EchList.TapUUID
		Tap = 'tap%s' % TapUUID[:11]
		operateinfo = {'action':'start','parame':{'EchId':self.params['EchId'],'VlanId':VlanId,'Tap':Tap}}
		print operateinfo
		KvmOperateOut = NcloudLib.HttpRequest(operateinfo,EchList['EchVncIp'],35796)
		print KvmOperateOut
		if KvmOperateOut['code'] == 0:
			return_data = KvmOperateOut
		else:
			return_data = {
				'code':100001,
				'msg': '对不起，暂时无法为您启动当前主机，谢谢。',
			}
		return return_data
	def EchReboot(self):
		EchList = LvsInfo.objects.get(EchId=self.params['EchId'])
		operateinfo = {'action':'reboot','parame':{'EchId':self.params['EchId'],}}
		KvmOperateOut = NcloudLib.HttpRequest(operateinfo,EchList['EchVncIp'],35796)
		if KvmOperateOut['code'] == 0:
			return_data = KvmOperateOut
		else:
			return_data = {
				'code':100001,
				'msg': '对不起，暂时无法为您重启当前主机，谢谢。',
			}
		return return_data
	def EchStop(self):
		EchList = LvsInfo.objects.get(EchId=self.params['EchId'])
		operateinfo = {'action':'shutdown','parame':{'EchId':self.params['EchId'],}}
		KvmOperateOut = NcloudLib.HttpRequest(operateinfo,EchList['EchVncIp'],35796)
		if KvmOperateOut['code'] == 0:
			return_data = KvmOperateOut
		else:
			return_data = {
				'code':100001,
				'msg': '对不起，暂时无法为您关闭当前主机，谢谢。',
			}
		return return_data
	def EchDestroy(self):
		EchList = LvsInfo.objects.get(EchId=self.params['EchId'])
		operateinfo = {'action':'destroy','parame':{'EchId':self.params['EchId'],}}
		KvmOperateOut = NcloudLib.HttpRequest(operateinfo,EchList['EchVncIp'],35796)
		if KvmOperateOut['code'] == 0:
			return_data = KvmOperateOut
		else:
			return_data = {
				'code':100001,
				'msg': '对不起，暂时无法为您强制关闭当前主机，谢谢。',
			}
		return return_data
