# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os
#导出数据结构模块
from api.models import *

from lib import NcloudCacheLib
from CacheConfigureParame import verifyCacheCfgParame
#操作cache类
class HandleCache:

    def __init__(self, Data,params):
        self.params = params
        self.Data = Data
    #创建cache类
    
    def CreateCache(self):
        return_data = {}
        if self.params['CacheMode'] == '0':
            return_data = NcloudCacheLib.Create_Redis_Cluster(self.Data,self.params)
        elif self.params['CacheMode'] == '1':
            return_data = NcloudCacheLib.Create_Redis(self.Data,self.params)
        elif self.params['CacheMode'] == '2':
            return_data = NcloudCacheLib.Create_Memcache(self.Data,self.params)
        return return_data


    def UpdateCacheParameters(self):
        #验证提交的值格式是否正常
        return_data = {
            "code" : 0,
            "msg" : "提交参数成功"
        }
        parameStatus = 0
        for parame in self.params['parameters']:
            verify_result = verifyCacheCfgParame(parame['name'],parame['value'])
            print verify_result
            if verify_result['code'] == 1:
                parameStatus = 1
                print '---------------'
                return_data={
                    "code" : 1,
                    "msg":  """消息格式错误, 非法的配置项[%s]值[%s], 有效范围为[%s]""" % (parame['name'],parame['value'],verify_result['msg']),
                }
                break
        if parameStatus == 0:
            CacheCgfDetails = CacheConfigureInfo.objects.filter(UserId=self.Data['UserId']).filter(CcfgId = self.params['cachecfgid']).first()
            for parame in self.params['parameters']:
                name = parame['name']
                nameList = name.split('-')
                try:
                    if nameList[1]:
                        name = name.replace('-','_')
                        CacheCgfDetails[name] = parame['value']
                except:
                    CacheCgfDetails[name] = parame['value']
            CacheCgfDetails.save()
                #parame['name'],parame['value']
        return return_data
    def ResetCacheParameters(self):
        return_data = {
            "code" : 0,
            "msg" : "提交重置参数成功"
        }
        CacheDefCfgDetails = CacheDefconfigureInfo.objects.filter(CcfgId=self.params['cachecfgid']).first()
        CacheCfgDetails = CacheConfigureInfo.objects.filter(CcfgId=self.params['cachecfgid']).first()
        CacheCfgkey = json.loads(CacheDefCfgDetails.to_json()).keys()
        CacheCfgkey.remove('_id')
        CacheCfgkey.remove('CcfgId')
        CacheCfgkey.remove('CcfgName')
        CacheCfgkey.remove('Bewrite')
        CacheCfgkey.remove('CfgSource')
        CacheCfgkey.remove('Category')
        CacheCfgkey.remove('Type')
        CacheCfgkey.remove('TypeName')
        CacheCfgkey.remove('CreateTime')
        for keys in CacheCfgkey:
            CacheCfgDetails[keys] = CacheDefCfgDetails[keys]
        CacheCfgDetails.save()
        #
        #for CacheDefCfg in xrange(len(CacheDefCfgDetails)):
        #   print CacheDefCfg
        return return_data
    def DescribeCacheCfgList(self):
        return_data = {}
        #类别为 Category = 0 并且属于当前用户的 or UserId = self.Data['UserId']
        CacheCfgList = []
        CacheCgfLists = CacheConfigureInfo.objects.filter(Type=self.params['cache_mode'])\
                                                                                .filter(UserId=self.Data['UserId'])
        if CacheCgfLists:
            for CacheCfgDetails in CacheCgfLists:
                CacheCfgDetail = dict(
                    cachecfgid = CacheCfgDetails['CcfgId'],
                    cachecfgname = CacheCfgDetails['CcfgName']
                )
                CacheCfgList.append(CacheCfgDetail)
            return_data['code'] = 0
            return_data['CacheCfgList'] = CacheCfgList
        else:
            return_data['code'] = 1030
            return_data['CacheCfgList'] = CacheCfgList
        return return_data
    def GainNodeMonitorData(self):
        #Querytime = datetime.datetime.now()-datetime.timedelta(minutes=120)
        if self.params['GainType'] == 'week':
            #EchData = NcloudNcm.HandleNcm(Data,params).Gain_ECH_CPU_Week_Data()
            pass
        elif self.params['GainType'] == 'month':
            pass
            #EchData = NcloudNcm.HandleNcm(Data,params).Gain_ECH_Month_Data()
        else:
            xdata = []
            ydata = {}
            #RecordDate__gt=Querytime
            CacheMonitorList = CacheNodeMonitorInfo.objects.filter(CacheNodeId=self.params['NodeId']).filter().order_by('-RecordDate')[0:120]
            ycpu = []
            ymem = []
            ydiskstrore = []
            ynetstkb = []
            ynetrvkb = []
            YUnit = ''
            yhitrati = []
            ytotleconn = []
            yconnclients = []
            yget = []
            yset = []
            ysetex = []
            ykeyex = []
            if CacheMonitorList:
                UnitList = []
                for CacheMonitorDetails in CacheMonitorList:
                    date = CacheMonitorDetails['RecordDate'].strftime("%Y-%m-%d %H:%M")
                    #XDate = '%s:%s' % (date.hour,date.minute)
                    #xdata.insert(0,XDate)
                    xdata.insert(0,date)
                    Monitor_data = json.loads(CacheMonitorDetails['Monitor_data'])
                    cpu = Monitor_data['cpu']['cpu_percent']
                    mem = Monitor_data['mem']['phymem_percent']
                    diskstrore = Monitor_data['diskstrore']['disk_percent']
                    netstkb = Monitor_data['netio']['net_sent_kb']
                    netrvkb = Monitor_data['netio']['net_recv_kb']
                    hitrati = Monitor_data['redis']['keyspace_percent']
                    totleconn = Monitor_data['redis']['Total_conn_recv']
                    connclients = Monitor_data['redis']['conn_clients']
                    get_num = Monitor_data['redis']['get_num']
                    set_num = Monitor_data['redis']['set_num']
                    setex_num = Monitor_data['redis']['setex_num']
                    keyex_num = Monitor_data['redis']['keyex_num']
                    ycpu.insert(0,cpu)
                    ymem.insert(0,mem)
                    ydiskstrore.insert(0,diskstrore)
                    ynetstkb.insert(0,netstkb)
                    ynetrvkb.insert(0,netrvkb)
                    UnitList.append(netstkb)
                    UnitList.append(netrvkb)
                    yhitrati.insert(0,hitrati)
                    ytotleconn.insert(0,totleconn)
                    yconnclients.insert(0,connclients)
                    yget.insert(0,get_num)
                    yset.insert(0,set_num)
                    ysetex.insert(0,setex_num)
                    ykeyex.insert(0,keyex_num)
                Unit = max(UnitList)
                if Unit > 1048576:
                    YUnit = 'M'
                elif Unit >1024:
                    YUnit = 'K'
                else:
                    YUnit = ''
            ynet = dict(
                ynetstkb = ynetstkb,
                ynetrvkb = ynetrvkb,
                YUnit = YUnit,
            )
            yoperand = dict(
                yget = yget,
                yset = yset,
                ysetex = ysetex,
                ykeyex = ykeyex,
            )
            MonitorData = dict(
                cpu = ycpu,
                mem = ymem,
                diskstrore = ydiskstrore,
                ynet = ynet,
                yhitrati = yhitrati,
                ytotleconn = ytotleconn,
                yconnclients = yconnclients,
                yoperand = yoperand,
            )
            ydata = MonitorData
            return_data ={
                'xdata' : xdata,
                'ydata' : ydata,
            }
        return return_data
