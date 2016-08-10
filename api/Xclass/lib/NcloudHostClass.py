#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
2016-04-06
shengyuan
Create plublish Host Class
判断KVM资源情况 剩余CPU 内存 判断所需镜像是否存在 获取VNC端口 更具所选私有网络获取IP地址
区域，cpu，mem，系统类型，镜像版本id，类型（ech，nlb，cache，），私用网络（VswId），
"""
import uuid
import hashlib


from api.models import *
from api.Nclass.lib import NcloudLib
class IMAGESDataHandle(object):


    def __init__(self):
        pass
    def ImageVerifiHandle(self,imagesid):
        #判断进行是否存在，
        ImageDetails= ImagesInfo.objects.filter(ImagesId = imagesid).first()
        if ImageDetails:
            ImagesPlatform = ImageDetails.ImagesPlatform
            if ImagesPlatform == 'linux':
                SystemVolume = 20
            else:
                SystemVolume = 40
            imageDetail = ImagesList.objects.filter(ImagesId=imagesid).filter(ImagesStatus=1).first()
            if imageDetail:
                #
                ImageInfo = dict(
                    ImagesId = imageDetail.ImagesName,
                    SYSPosition = imageDetail.SYSPosition,
                    DiskPosition = imageDetail.SYSPosition,
                    ImagesPosition = imageDetail.ImagesPosition,
                    PoolId = imageDetail.PoolId,
                    ImagesListId = imageDetail.id,
                    SystemVolume = SystemVolume,
                )
                #imageDetail.ImagesStatus = 0
                #imageDetail.save()
                return_data = {
                    "code" : 0,
                    "msg" : "action completed successful",
                    "ImageInfo" : ImageInfo,
                }
            else:
                return_data = {
                    "code" : 1003,
                    "msg" : "action completed fails",
                }
        else:
            return_data = {
                "code" : 1002,
                "msg" : "action completed fails",
            }
        return return_data

    def EditImagesListStatus(self,imagelistid):


        ImagesDetails = ImagesList.objects.filter(id=imagelistid).first()
        if ImagesDetails:
            ImagesDetails.ImagesStatus = 0
            ImagesDetails.save()
            return_data = {
                "code" : 0,
                "msg" : "action completed successful",
            }
        else:
            return_data = {
                "code" : 1006,
                "msg" : "action completed fails",
            }
        return return_data

class IMAGESStrongeHandle(object):


    def __init__(self,parame):
        self.parame = parame

    def MvImageHandle(self,zone,gfsId,imageslistid):

        # 读取本地 存储list地址 如果地址为等于二 则 for  循环判断
        GfsList = GfsInfo.objects.filter(Zone=zone).filter(GfsId=gfsId) # PoolId
        GfsIps = ''
        GfsIpList = []
        if GfsList:
            MvInfo = {
                'action':'MvEchInfo',
                'parame':self.parame,
            }
            for g in xrange(len(GfsList)):
                GfsIp = GfsList[g].GfsIp
                print MvInfo
                MvEchStatus = NcloudLib.HttpRequest(MvInfo,GfsIp,35796)
                print MvEchStatus
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
                        DelStatus = self.DelImageHandle(GfsIps)
                        #MvEchStatus = NcloudLib.HttpRequest(DeleteEchImages,GfsIps,35796)
                        GfsIps = ''
            if GfsIps == '':
                #移动images文件失败
                return_data = {
                    "code" : 1007,
                    "msg" : "action completed fails",
                }
            else:
                #移动文件成功
                #调用ImagesHandle 更改状态
                IMAGESDataHandle().EditImagesListStatus(imageslistid)

                return_data = {
                    "code": 0,
                    "msg" : "action completed successful",
                    "GfsIpList" : GfsIpList,
                }
        else:
            return_data = {
                    "code" : 1004,
                    "msg" : "action completed fails",
            }
        return return_data

        def  DelImageHandle(self,gfsIps):
            DelInfo = {
                'action':'DeleteEchImages',
                'parame':self.parame,
            }
            DelImageStatus = NcloudLib.HttpRequest(DelInfo,gfsIps,35796)
            if DelImageStatus['code'] == 0:
                return_data = {
                    "code" : 0,
                    "msg" : "action completed successful",
                }
            else:
                return_data = {
                    "code" : 1005,
                    "msg" : "action completed fails",
                }
            return return_data

class HandleHost(object):


    def __init__(self,Data,params):
        self.params = params
        self.Data = Data

    def CreateEch(self):

        return_data = {
            "code" : 1000,
            "msg"  : "action completed fails"
        }

        KvmHandle = KvmDataHandle(self.Data,self.params)
        VerificationKVMStatus = KvmHandle.KvmVerifiHandle()
        if VerificationKVMStatus['code'] != 0:
            pass
        else:
            #kvm 有资源供创建当前资源
            #根据imageID 获取 当前ImagesInfo资源信息
            ImageHandle = IMAGESDataHandle()
            VerificationImageStatus = ImageHandle.ImageVerifiHandle(self.params['image_id'])
            if VerificationImageStatus['code'] != 0:
                KvmHandle.KvmDataEditHandle(VerificationKVMStatus['kvmid'])
                pass
            else:
                #获取 HostInfo
                HostHandle = HostDataHandle(self.params['vswid'],self.params['HostType'])
                HostHandleStatus = HostHandle.HostInfoBuild(Zone=self.Data['Zone'])
                if HostHandleStatus['code'] != 0:
                    KvmHandle.KvmDataEditHandle(VerificationKVMStatus['kvmid'])
                    pass
                else:
                    #移动镜像
                    if self.params['HostType'] == 'ech':
                        TypeName = 'instances'
                        Type = 0
                    elif self.params['HostType'] =='cache':
                        TypeName = 'cache'
                        Type = 1
                    parame = {
                            'EchId':HostHandleStatus['HostInfo']['HostId'],
                            'ImagesPosition':VerificationImageStatus['ImageInfo']['ImagesPosition'],
                            'ImagesId':VerificationImageStatus['ImageInfo']['ImagesId'],
                            'EchUUID':HostHandleStatus['HostInfo']['HostUUID'],
                            'HostType':TypeName,
                    }
                    #创建 Host 镜像文件
                    ImageHandle = IMAGESStrongeHandle(parame)
                    MvImage_Result = ImageHandle.MvImageHandle(self.Data['Zone'],VerificationImageStatus['ImageInfo']['PoolId'],
                                                                                                            VerificationImageStatus['ImageInfo']['ImagesListId'])
                    print MvImage_Result
                    # 如果移动镜像文件成功则创建Host libvirt xml 文件
                    if MvImage_Result['code'] == 0:
                        operateinfo = {
                            'action':'Create_ech',
                            'parame':{
                                'EchId':HostHandleStatus['HostInfo']['HostId'],
                                'EchName':HostHandleStatus['HostInfo']['HostName'],
                                'EchCpu':int(self.params['cpu']),
                                'EchMem':int(self.params['memory']),
                                'EchUUID':HostHandleStatus['HostInfo']['HostUUID'],
                                'TapUUID':HostHandleStatus['HostInfo']['TapUUID'],
                                'Tap':HostHandleStatus['HostInfo']['Tap'],
                                'EchVNCPort':HostHandleStatus['HostInfo']['VNCPort'],
                                'EchIp':HostHandleStatus['HostInfo']['HostIp'],
                                'EchPlatform':VerificationImageStatus['ImageInfo']['ImagesPosition'],
                                'ImagesId':VerificationImageStatus['ImageInfo']['ImagesId'],
                                'ImagesPosition':VerificationImageStatus['ImageInfo']['SYSPosition'],
                                'SYSPosition':VerificationImageStatus['ImageInfo']['SYSPosition'],
                                'EchMac':HostHandleStatus['HostInfo']['HostMac'],
                                'HostType':TypeName,
                            },
                        }
                        #创建云主机
                        #发送至KVM主机创建
                        CreateHost_Result = NcloudLib.HttpRequest(operateinfo,VerificationKVMStatus['KVMIp'],35796)
                        print CreateHost_Result
                        #print Status
                        #如果创建成功 则生成disk磁盘数据
                        if CreateHost_Result['code'] == 0:
                            # 生成磁盘数据
                            #DISKDataHandle()
                            #生成DISKUUID =
                            DiskUUID = str(uuid.uuid1())
                            DiskId = 'd-%s' % DiskUUID[:8]
                            DiskName = 'DZ%sZ' % DiskUUID[:8]
                            DiskInfo(DiskId=DiskId,DiskName=DiskName,DiskVolume=VerificationImageStatus['ImageInfo']['SystemVolume'],
                                            DiskZone=VerificationImageStatus['ImageInfo']['PoolId'],DiskPosition=VerificationImageStatus['ImageInfo']['DiskPosition'],
                                            DiskMount='vda',DiskAttr='system',EchId=HostHandleStatus['HostInfo']['HostId'],UserId=self.Data['UserId']).save()
                            HostInfo = dict(
                                HostId=HostHandleStatus['HostInfo']['HostId'],
                                HostName=HostHandleStatus['HostInfo']['HostName'],
                                HostIp=HostHandleStatus['HostInfo']['HostIp'],
                                KVMIp=VerificationKVMStatus['KVMIp'],
                                VNCPort=HostHandleStatus['HostInfo']['VNCPort'],
                                HostMac=HostHandleStatus['HostInfo']['HostMac'],
                                TapUUID=HostHandleStatus['HostInfo']['TapUUID'],
                                HostUUID=HostHandleStatus['HostInfo']['HostUUID'],
                                TenantId=HostHandleStatus['HostInfo']['TenantId'],
                                VlanId=HostHandleStatus['HostInfo']['SegmentationId'],
                            )
                            """
                            if HostType == 'ech':
                                inHost = EchInfo(EchId=HostHandleStatus['HostInfo']['HostId'],EchName=HostHandleStatus['HostInfo']['HostName'],
                                                        EchBewrite='',EchZone=self.Data['Zone'],EchCpu=int(self.params['cpu']),
                                                        EchMemory=int(self.params['memory']),ImageId=self.params['image_id'],
                                                        EchIp=HostHandleStatus['HostInfo']['HostIp'],EchVncIp=VerificationKVMStatus['KVMIp'],
                                                        EchVncPort=HostHandleStatus['HostInfo']['VNCPort'],EchPaymentType=0,EchPaymentDate=0,
                                                        EchMacs=HostHandleStatus['HostInfo']['HostMac'],TapUUID=HostHandleStatus['HostInfo']['TapUUID'],
                                                        EchUUID=HostHandleStatus['HostInfo']['EchUUID'],TenantId=HostHandleStatus['HostInfo']['TenantId'],
                                                        VlanId=HostHandleStatus['HostInfo']['SegmentationId'],UserId=self.Data['UserId'])
                            if HostType == 'cache':

                            inHost.save()
                            """
                            HASHHandel().BuildVNCToken(self.Data['UserId'],VerificationKVMStatus['KVMIp'],HostHandleStatus['HostInfo']['VNCPort'])
                            # 添加数据至所属私用网络中
                            operateinfo = {
                                'action':'AddEchToSwitch',
                                'parame':{
                                    'EchName':HostHandleStatus['HostInfo']['HostName'],
                                    'EchMacs':HostHandleStatus['HostInfo']['HostMac'],
                                    'EchIp':HostHandleStatus['HostInfo']['HostIp'],
                                    'Qdhcp':HostHandleStatus['HostInfo']['Qdhcp'],
                                    'Type':0,
                                }
                            }
                            HostOperateOut =  NcloudLib.HttpRequest(operateinfo,'127.0.0.1',35796)
                            print HostOperateOut
                            if HostOperateOut['code'] == 0:
                                #添加数据至私有网络列表中
                                VpcSwitchHostInfo(HostId = HostHandleStatus['HostInfo']['HostId'],VswId = self.params['vswid'],
                                                                HostIp = HostHandleStatus['HostInfo']['HostIp'],Status = 1,Type = Type,TypeName = TypeName,
                                                                Zone = self.Data['Zone'],UserId = self.Data['UserId'],).save()
                                return_data = {
                                    'code':0,
                                    'Status': '恭喜，创建云主机成功。',
                                    'msg' : '恭喜，创建云主机成功。',
                                    "HostInfo":HostInfo,
                                }
                            else:
                                return_data = {
                                    'code':0,
                                    'Status': '对不起，加入私用网络失败，请手动加入。',
                                    'msg' : '恭喜，创建云主机成功。',
                                    "HostInfo":HostInfo,
                                }
                            #创建EHC云主机结束
                        else:
                            #创建 host libvirt xml 失败，删除images文件，增加 KVM 剩余资源配置
                            for Gfsip in MvImage_Result['GfsIpList']:
                                ImageHandle.DelImageHandle(Gfsip)
                            KvmHandle.KvmDataEditHandle(VerificationKVMStatus['kvmid'])
                            return_data = {
                                'code':100002,
                                'Status': '无法创建移动用主机镜像文件',
                                'msg' : '对不起，暂时无法为您创建主机，请稍后再试，谢谢',
                            }
        return return_data

class HASHHandel(object):


    """docstring for MD5Handel
    md5 生成
    生成vnc 链接token id
    """
    import hashlib
    def __init__(self):
        pass

    def  BuildMD5(self,buildstr):

        return hashlib.md5(buildstr).hexdigest()
        # print hashlib.sha1(a).hexdigest()
        # print hashlib.sha224(a).hexdigest()
        # print hashlib.sha256(a).hexdigest()
        # print hashlib.sha384(a).hexdigest()
        # print hashlib.sha512(a).hexdigest()

    def BuildVNCToken(self,userid,KVMIp,VNCPort):

        UserVncId = UserInfo.objects.filter(id=userid).first()
        vncpasstoken = "%s%s%s" %(UserVncId.VNCPasswd,'NDZ',VNCPort)
        token = '%s: %s:%s\n' % (self.BuildMD5(vncpasstoken),KVMIp,VNCPort)
        with open("vnc_tokens",'a') as f:
            f.write(token)
        return_data = {
            "code" : 0,
            "msg" : "action completed successful",
        }
        return return_data

class HostDataHandle(object):


    def __init__(self,vswid,HostType):
        #pass
        # vswid , HostType
        self.vswid = vswid
        self.HostType = HostType

    def HostInfoBuild(self,Zone):

        #生成ECH数据
        #生成EchIp 获取当前
        return_data = {
            "code" : 1003,
            "msg" : "action completed fails",
        }
        SwitchDetails = VpcSwitch.objects.filter(VswId=self.vswid).first()
        if SwitchDetails:
            TenantId = SwitchDetails.TenantId
            DnsmasqxIp = SwitchDetails.DnsmasqxIp
            UsableIp = SwitchDetails.UsableIp
            Qdhcp = SwitchDetails.Qdhcp
            VpcDetails = VpcInfo.objects.get(TenantId=TenantId)
            SegmentationId = VpcDetails.SegmentationId
            #获取最大数-以使用地址
            VSHList = VpcSwitchHostInfo.objects.filter(VswId=self.vswid).order_by('-CreateTime').first()
            if VSHList:
                VSHostIp = VSHList.HostIp
                if int(VSHostIp.split('.')[3]) >= UsableIp:
                    return return_data
                else:
                    print VSHostIp
                    HostIp = '%s.%s.%s.%s' % (VSHostIp.split('.')[0],VSHostIp.split('.')[1],VSHostIp.split('.')[2],int(VSHostIp.split('.')[3])+1)
            else:
                #不存在则为其实+1
                HostIp = '%s.%s.%s.%s' % (DnsmasqxIp.split('.')[0],DnsmasqxIp.split('.')[1],
                                                                DnsmasqxIp.split('.')[2],int(DnsmasqxIp.split('.')[3])+1)
            #NetEchNumList = EchInfo.objects.filter(TenantId=TenantId)
            #生成ECHUUID
            HostUUID = str(uuid.uuid1())
            #生成 tapUUID
            TapUUID = str(uuid.uuid1())
            #获取 VNC 端口 #更具端口序列插叙 最大一个 + 1
            #根据类型获取不同类型端口 ECH EchInfo 表 59001开始 Cahce CacheNodeInfo 表 62001端口 Nlb LbsInfo表 49001开始
            if self.HostType == 'ech':
                #生成ECHID
                HostId = 'i-%s' % HostUUID[:8]
                #生成ECHNAME
                HostName = 'iZ%sZ' % HostId.split('-')[1]
                VncLish = EchInfo.objects.filter(EchZone=Zone).order_by('-EchVncPort').first()
                if VncLish:
                    VNCPort = VncLish['EchVncPort'] +1
                else:
                    VNCPort = 59001
            if self.HostType == 'cache':
                VncLish = CacheNodeInfo.objects.filter(Zone=Zone).order_by('-VncPort').first()
                if VncLish:
                    VNCPort = VncLish['VncPort'] +1
                else:
                    VNCPort = 62001
                #生成ECHID
                HostId = 'cn-%s' % HostUUID[:8]
                #生成ECHNAME
                HostName = 'CN%sZ' % HostId.split('-')[1]

            #生成ECHNETID
            Tap = 'tap%s' % TapUUID[:11]
            #生成MAC地址
            HostMac = NcloudLib.buildMac()
            HostInfo = dict(
                HostIp = HostIp,
                HostUUID = HostUUID,
                TapUUID = TapUUID,
                HostId = HostId,
                HostName = HostName,
                VNCPort = VNCPort,
                Tap = Tap,
                HostMac = HostMac,
                TenantId = TenantId,
                SegmentationId = SegmentationId,
                Qdhcp = Qdhcp,
            )
            return_data = {
                "code" : 0,
                "msg" : "action completed successful",
                "HostInfo" : HostInfo,
            }
        return return_data

class KvmDataHandle(object):


    def __init__(self,Data,params):
        self.params = params
        self.Data = Data

    def KvmVerifiHandle(self):
        #处理 KVM方法 及保存数据方法
        kvmDetails = KvmInfo.objects.filter(KVMArea=self.Data['Zone']).filter(KVMSurplusCpu__gte=int(self.params['cpu']))\
                                                                    .filter(KVMSurplusMem__gte=int(self.params['memory'])).order_by('-KVMSurplusCpu').first()
        if kvmDetails:
            #输出是否存在可用资源  如果存在则输入id
            kvmDetails.KVMSurplusCpu = kvmDetails.KVMSurplusCpu - int(self.params['cpu'])
            kvmDetails.KVMSurplusMem = kvmDetails.KVMSurplusMem - int(self.params['memory'])
            kvmDetails.save()
            return_data = {
                "code" : 0,
                "kvmid" : kvmDetails.id,
                "msg" :"action completed successful",
                "KVMIp" : kvmDetails.KVMIp,
            }
        else:
            """
            return_data = {
                'code':100002,
                'Status': 'KVM剩余CPU或MEM不足',
                'msg' : '对不起，暂时无法为您创建主机，请稍后再试，谢谢',
            }
            """
            return_data = {
                "code" : 1001,
                "msg" : "action completed fails",
            }

        return return_data
    def KvmDataEditHandle(self,kvmid):
        KvmDetails = KvmInfo.objects.get(id=kvmid)
        KvmDetails.KVMSurplusCpu = KvmDetails.KVMSurplusCpu + int(self.params['cpu'])
        KvmDetails.KVMSurplusMem = KvmDetails.KVMSurplusMem + int(self.params['memory'])
        KvmDetails.save()
        return_data = {
            "code" : 0,
            "msg" : "action completed successful",
        }
        return return_data
