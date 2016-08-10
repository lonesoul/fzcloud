# coding=utf-8

#导入常用模块
import datetime,json,md5,sys,os,time
#导入数据结构模块
from api.models import *
#导入常用类
from lib import NcloudLib
#from lib import NcloudReleaseLib
import requests
import uuid
#导入hashlib模块
import hashlib
#操作HandleLogs类
class HandleSnapshot:

	def __init__(self, Data,params):
		self.params = params
		self.Data = Data
	def BackEchSysDisk(self):
		#snapid EchId /dir type 是否挂载
		DiskType = 'system'
		DiskDetails = DiskInfo.objects.filter(EchId=self.params['EchId']).filter(DiskAttr=DiskType)
		for DiskDetail in DiskDetails:
			DiskId = DiskDetail['DiskId']
			DiskVolume = DiskDetail['DiskVolume']
			DiskZone = DiskDetail['DiskZone']
			DiskPosition = DiskDetail['DiskPosition']
			DiskAttr = DiskDetail['DiskAttr']
			
		EchDetail = EchInfo.objects.get(EchId=self.params['EchId'])
		DiskKVMIp = EchDetail['EchVncIp']
		#更具EchId 查询 disk_info 获取diskId diskVolume diskZone diskPosition diskAttr  
		#计算 diskDir = diskPosition+ EchId + '.img'
		DiskDir = DiskPosition+ self.params['EchId'] + '.img'
		MountStatus = 1
		SnapUid = str(uuid.uuid1())
		params = {
			"action":"BackUpSnapshot",
			"parame":{
				"SnapUid":SnapUid,
				"DiskId" :DiskId,
				"DiskVolume":DiskVolume,
				"DiskDir":DiskDir,
				"DiskType":DiskType,
				"MountStatus":MountStatus,
				"EchId":self.params['EchId'],
			}
		}
		print params
		params = json.dumps(params)
		url = 'http://' + DiskKVMIp + ':35796/'
		print url
		r = requests.post(url,data=params)
		if r.json()['code'] == 0:
			#插入数据
			#计算snapid
			#获取 Snapshot 信息
			
			SnapLish = SnapshotInfo.objects.all().order_by('-CreateTime')[0:1]
			if SnapLish:
				print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
				for Snap in SnapLish:
					SnapRawId = Snap.SnapId
					print SnapRawId
				SnapRawNum = SnapRawId.split('-')
				#生成SnapId
				SnapNum = int(SnapRawNum[1]) + 1
				print SnapNum
				#生成SnapID
				SnapId = 's-%s' % SnapNum
				print SnapId
			else:
				SnapNum = 1000001
				#生成ECHID
				SnapId = 's-%s' % SnapNum
			'''
			RandomNum=NcloudLib.getRandomNum(9)
			SnapId = 's-' + RandomNum
			'''
			insnapshot = SnapshotInfo(SnapId=SnapId,SnapName=self.params['backName'],SnapStatus=1,DiskId=DiskId,DiskVolume=DiskVolume,DiskAttr=DiskAttr,SnapResource=self.params['EchId'],SnapUid=SnapUid,SnapPattern='virsh',DiskKVMIp=DiskKVMIp)
			insnapshot.save()
			return_data = {
				"code": 0,
				"mgs" : "备份成功！",
			}
		else:
			return_data = {
				"code": r.json()['code'],
				"mgs" : "对不起，暂时无法为您完成备份，请稍后重试！",
			}
		return return_data
	def DeleteSnapshot(self):
		#根据snapid查询 snapuid diskkvmip 判断备份方式 获取挂载EchId  查询备份方式 
		#已经挂载 备份方式为virsh-》  virsh snapshot-delete EchId snapuid
		#备份方式为 qemu-img qemu-img snapshot -d snapuid img路径
		SnapDetail = SnapshotInfo.objects.get(SnapId=self.params['snapshotid'])
		DiskKVMIp = SnapDetail['DiskKVMIp']
		EchId = SnapDetail['SnapResource']
		SnapUid = SnapDetail['SnapUid']
		SnapPattern = SnapDetail['SnapPattern']
		#if SnapDetail['SnapPattern'] == 'qemu':
		#	
		params = {
			"action":"DeleteSnapshot",
			"parame":{
				"SnapUid":SnapUid,
				"EchId":EchId,
				"SnapPattern":SnapPattern,
			}
		}
		print params
		params = json.dumps(params)
		url = 'http://' + DiskKVMIp + ':35796/'
		r = requests.post(url,data=params)
		if r.json()['code'] == 0:
			SnapDetail.delete()
			return_data = {
				"code": 0,
				"mgs" : "删除备份成功！",
			}
		else:
			return_data = {
				"code": r.json()['code'],
				"mgs" : "对不起，暂时无法为您完成备份，请稍后重试！",
			}
		return return_data
	def RecoverSnapshot(self):
		#根据SnapId 查询 判断当前备份类型 如果是
		SnapDetail = SnapshotInfo.objects.get(SnapId=self.params['snapshotid'])
		DiskKVMIp = SnapDetail['DiskKVMIp']
		SnapUid = SnapDetail['SnapUid']
		DiskAttr = SnapDetail['DiskAttr']
		SnapResource = SnapDetail['SnapResource']
		if DiskAttr == 'system':
			params = {
				"action":"RecoverSnapshot",
				"parame":{
					"SnapUid":SnapUid,
					"EchId":SnapResource,
				}
			}
		else:
			pass
		params = json.dumps(params)
		url = 'http://' + DiskKVMIp + ':35796/'
		r = requests.post(url,data=params)
		if r.json()['code'] == 0:
			return_data = {
				"code": 0,
				"mgs" : "恢复备份成功！",
			}
		else:
			return_data = {
				"code": r.json()['code'],
				"mgs" : "对不起，暂时无法为您完成快照恢复备份，请稍后重试！",
			}
		return return_data