# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os
#导出数据结构模块
from api.models import *
from bson import json_util
from lib import NcloudMonitorLib

#操作Monitor类
class HandleNcm:

	def __init__(self, Data,params):
		self.params = params
		self.Data = Data
	#获取一周内数据
	def Gain_ECH_CPU_Week_Data(self):
		'''
		NCMEchWeek=db.ncm_ech_cpu_week_info.find().sort('RecordDate')
		#print NCMEchWeek.count()
		#print NCMEchWeek.count()/30
		'''
		#获取当前日期及七天内每天日期
		NowDateTime = datetime.datetime.now()
		ydata = []
		xdata = []
		#for i in xrange(7):
		for i in xrange(7):
			#print datetime.datetime.now()
			Days = i + 1
			d1 = NowDateTime + datetime.timedelta(days = -Days)
			'''
			date_to_0 = datetime.datetime(d1.year,d1.month,d1.day,5,59,59)
			date_from_0 = datetime.datetime(d1.year,d1.month,d1.day,0,0,0)
			date_to_1 = datetime.datetime(d1.year,d1.month,d1.day,11,59,59)
			date_from_1 = datetime.datetime(d1.year,d1.month,d1.day,6,0,0)
			date_to_2 = datetime.datetime(d1.year,d1.month,d1.day,17,59,59)
			date_from_2 = datetime.datetime(d1.year,d1.month,d1.day,12,0,0)
			date_to_3 = datetime.datetime(d1.year,d1.month,d1.day,23,59,59)
			date_from_3 = datetime.datetime(d1.year,d1.month,d1.day,18,0,0)
			'''
			#分段执行时段列表
			DateMeet = []
			for j in xrange(4):
				Hours_from = j * 6
				Hours_to = Hours_from + 5
				Hour = (Hours_to + 1)/2
				date_from = datetime.datetime(d1.year,d1.month,d1.day,Hours_from,0,0)
				date_to = datetime.datetime(d1.year,d1.month,d1.day,Hours_to,59,59)
				date_Hour = datetime.datetime(d1.year,d1.month,d1.day,Hour,0,0).strftime('%m-%d %H')
				#xdata.append(date_Hour)
				DateDirt = {
					 'date_from' : date_from,
					 'date_to' : date_to,
					 'date_Hour' : date_Hour,
				}
				DateMeet.append(DateDirt)
			#查询日期列表倒序
			DateMeet.reverse()
			#根据时间获取时间段内平均数据百分比
			for DateClass in DateMeet:
				#print DateClass
				NcmEchWeekDetails = NcmEchCpuWeekInfo.objects.filter(EchId=self.params['EchId']).filter(RecordDate__gte=DateClass['date_from'],RecordDate__lte=DateClass['date_to'])
				#NcmEchWeekDetails = NcmEchCpuWeekInfo.objects.filter(RecordDate__gte=DateClass['date_from'],RecordDate__lte=DateClass['date_to'])
				'''
				PercentSum = 0
				
				for NcmEchWeek in NcmEchWeekDetails:
					PercentSum += NcmEchWeek['CpuPercent']
				print PercentSum
				'''
				PercentSum = NcmEchWeekDetails.sum('CpuPercent')
				try:
					NcmEchWeekPercent = float('%0.1f'%(PercentSum/NcmEchWeekDetails.count()))
				except:
					NcmEchWeekPercent = 0
				#print DateClass['date_Hour']
				xdata.append(DateClass['date_Hour'])
				ydata.append(NcmEchWeekPercent)
		ydata.reverse()
		xdata.reverse()
		return_data = {
			"ydata" : ydata,
			"xdata" : xdata,
		}
		return_data = json.dumps(return_data)
		return return_data
	def Gain_ECH_MEM_Week_Data(self):
		#获取当前日期及七天内每天日期
		NowDateTime = datetime.datetime.now()
		ydata = []
		xdata = []
		for i in range(7):
			Days = i + 1
			d1 = NowDateTime + datetime.timedelta(days = -Days)
			#分段执行时段列表
			DateMeet = []
			for j in range(4):
				Hours_from = j * 6
				Hours_to = Hours_from + 5
				Hour = (Hours_to + 1)/2
				date_from = datetime.datetime(d1.year,d1.month,d1.day,Hours_from,0,0)
				date_to = datetime.datetime(d1.year,d1.month,d1.day,Hours_to,59,59)
				date_Hour = datetime.datetime(d1.year,d1.month,d1.day,Hour,0,0).strftime('%m-%d %H')
				#xdata.append(date_Hour)
				DateDirt = {
					 'date_from' : date_from,
					 'date_to' : date_to,
					 'date_Hour' : date_Hour,
				}
				DateMeet.append(DateDirt)
			#查询日期列表倒序
			DateMeet.reverse()
			#根据时间获取时间段内平均数据百分比
			for DateClass in DateMeet:
				#print DateClass
				NcmEchWeekDetails = NcmEchMemWeekInfo.objects.filter(EchId=self.params['EchId']).filter(RecordDate__gte=DateClass['date_from'],RecordDate__lte=DateClass['date_to'])
				#print NcmEchWeekDetails.count()
				'''
				PercentSum = 0
				for NcmEchWeek in NcmEchWeekDetails:
					PercentSum += NcmEchWeek['MemUsaPercent']
				'''
				PercentSum = NcmEchWeekDetails.sum('MemUsaPercent')
				try:
					NcmEchWeekPercent = float('%0.1f'%(PercentSum/NcmEchWeekDetails.count()))
				except:
					NcmEchWeekPercent = 0
				#print DateClass['date_Hour']
				xdata.append(DateClass['date_Hour'])
				ydata.append(NcmEchWeekPercent)
		ydata.reverse()
		xdata.reverse()
		return_data = {
			"ydata" : ydata,
			"xdata" : xdata,
		}
		return_data = json.dumps(return_data)
		return return_data
	def Gain_ECH_DISK_STRONG_Week_Data(self):
		#获取当前日期及七天内每天日期
		NowDateTime = datetime.datetime.now()
		ydata = []
		xdata = []
		for i in range(7):
			Days = i + 1
			d1 = NowDateTime + datetime.timedelta(days = -Days)
			#分段执行时段列表
			DateMeet = []
			for j in range(4):
				Hours_from = j * 6
				Hours_to = Hours_from + 5
				Hour = (Hours_to + 1)/2
				date_from = datetime.datetime(d1.year,d1.month,d1.day,Hours_from,0,0)
				date_to = datetime.datetime(d1.year,d1.month,d1.day,Hours_to,59,59)
				date_Hour = datetime.datetime(d1.year,d1.month,d1.day,Hour,0,0).strftime('%m-%d %H')
				#xdata.append(date_Hour)
				DateDirt = {
					 'date_from' : date_from,
					 'date_to' : date_to,
					 'date_Hour' : date_Hour,
				}
				DateMeet.append(DateDirt)
			#查询日期列表倒序
			DateMeet.reverse()
			#根据时间获取时间段内平均数据百分比
			for DateClass in DateMeet:
				#print DateClass
				NcmEchWeekDetails = NcmEchDiskStrongWeekInfo.objects.filter(EchId=self.params['EchId']).filter(RecordDate__gte=DateClass['date_from'],RecordDate__lte=DateClass['date_to'])
				#print NcmEchWeekDetails.count()
				'''
				PercentSum = 0
				for NcmEchWeek in NcmEchWeekDetails:
					PercentSum += NcmEchWeek['DiskUsedPercent']
				'''
				PercentSum = NcmEchWeekDetails.sum('DiskUsedPercent')
				try:
					NcmEchWeekPercent = float('%0.1f'%(PercentSum/NcmEchWeekDetails.count()))
				except:
					NcmEchWeekPercent = 0
				#print DateClass['date_Hour']
				xdata.append(DateClass['date_Hour'])
				ydata.append(NcmEchWeekPercent)
		ydata.reverse()
		xdata.reverse()
		return_data = {
			"ydata" : ydata,
			"xdata" : xdata,
		}
		return_data = json.dumps(return_data)
		return return_data
		
		
	def Gain_ECH_Month_Data(self):
		#获取当前日期及三十天内每天日期
		NowDateTime = datetime.datetime.now()
		ydata = []
		xdata = []
		#dx1= NowDateTime + datetime.timedelta(days = -1)
		#dx30= NowDateTime + datetime.timedelta(days = -30)
		
		#date_fromx = datetime.datetime(dx1.year,dx1.month,dx1.day,0,0,0)
		#date_tox = datetime.datetime(dx30.year,dx30.month,dx30.day,23,59,59)
		#print date_fromx
		#print '---------------------------'
		#print datetime.datetime.now()
		#NcmEchMonthDetails = NcmEchCpuMonthInfo.objects.filter(EchId=self.params['EchId']).filter(RecordDate__gte=date_tox,RecordDate__lte=date_fromx)
		#NcmEchMonthDetails = NcmEchCpuMonthInfo.objects.to_json()
		#print type(NcmEchMonthDetails)
		#print len(NcmEchMonthDetails)
		#print datetime.datetime.now()
		#NcmEchMonthDetails = json_util.dumps(NcmEchMonthDetails._query)
		#NcmEchMonthDetails = json_util.loads(NcmEchMonthDetails._collection.find(NcmEchMonthDetails._query))
		#print type(NcmEchMonthDetails)
		#print '-------------------------'
		#NcmEchMonthDetails = json_util.dumps(NcmEchCpuMonthInfo._collection.find(NcmEchCpuMonthInfo._query))

		
		#NcmEchMonthDetails = NcmEchCpuMonthInfo.objects.to_json()
		
		#filter(EchId=self.params['EchId']).filter(RecordDate__gte=date_tox,RecordDate__lte=date_fromx)
		#NcmEchMonthSum = NcmEchMonthDetails.sum('CpuPercent')
		for i in range(30):
			Days = i + 1
			d1 = NowDateTime + datetime.timedelta(days = -Days)
			#分段执行时段列表
			date_from = datetime.datetime(d1.year,d1.month,d1.day,0,0,0)
			date_to = datetime.datetime(d1.year,d1.month,d1.day,23,59,59)
			
			#定义时间轴日期
			date_Hour = date_from.strftime('%m-%d')
			xdata.append(date_Hour)
			#print NcmEchMonthDetails.count()
			#print type(NcmEchMonthDetails)
			#NcmEchMonthDetail = NcmEchMonthDetails.to_mongo()
			#len(NcmEchMonthDetail)
			#NcmEchMonthDetails.sum('CpuPercent')
			#NcmEchMonthDetails = NcmEchMonthDetails.filter(RecordDate__gte=date_from,RecordDate__lte=date_to).average('CpuPercent')
			#NcmEchMonthDetails=NcmEchMonthDetail.delete()

			#根据时间获取时间段内平均数据百分比
			#NcmEchMonthDetails = NcmEchCpuMonthInfo.objects.filter(EchId=self.params['EchId']).filter(RecordDate__gte=date_from,RecordDate__lte=date_to)
			#PercentSum = NcmEchMonthDetails.sum('CpuPercent')
			NcmEchMonthDetails = NcmEchMonthInfo.objects.filter(MonitorType=self.params['MonitorType']).filter(EchId=self.params['EchId']).filter(RecordDate=date_from)
			if NcmEchMonthDetails:
				for NcmEchMonthDetail in NcmEchMonthDetails:
					NcmEchMonthPercent = NcmEchMonthDetail['Percent']
			else:
				NcmEchMonthPercent = 0
			'''
			try:
				NcmEchMonthPercent = float('%0.1f'%(PercentSum/NcmEchMonthDetails.count()))
			except:
				NcmEchMonthPercent = 0
			'''
			ydata.append(NcmEchMonthPercent)

		ydata.reverse()
		xdata.reverse()
		return_data = {
			"ydata" : ydata,
			"xdata" : xdata,
		}
		return_data = json.dumps(return_data)
		return return_data
		
	def Gain_ECH_CPU_Month_Data(self):
		#获取当前日期及三十天内每天日期
		NowDateTime = datetime.datetime.now()
		ydata = []
		xdata = []
		#dx1= NowDateTime + datetime.timedelta(days = -1)
		#dx30= NowDateTime + datetime.timedelta(days = -30)
		
		#date_fromx = datetime.datetime(dx1.year,dx1.month,dx1.day,0,0,0)
		#date_tox = datetime.datetime(dx30.year,dx30.month,dx30.day,23,59,59)
		#print date_fromx
		#print '---------------------------'
		#print datetime.datetime.now()
		#NcmEchMonthDetails = NcmEchCpuMonthInfo.objects.filter(EchId=self.params['EchId']).filter(RecordDate__gte=date_tox,RecordDate__lte=date_fromx)
		#NcmEchMonthDetails = NcmEchCpuMonthInfo.objects.to_json()
		#print type(NcmEchMonthDetails)
		#print len(NcmEchMonthDetails)
		#print datetime.datetime.now()
		#NcmEchMonthDetails = json_util.dumps(NcmEchMonthDetails._query)
		#NcmEchMonthDetails = json_util.loads(NcmEchMonthDetails._collection.find(NcmEchMonthDetails._query))
		#print type(NcmEchMonthDetails)
		#print '-------------------------'
		#NcmEchMonthDetails = json_util.dumps(NcmEchCpuMonthInfo._collection.find(NcmEchCpuMonthInfo._query))

		
		#NcmEchMonthDetails = NcmEchCpuMonthInfo.objects.to_json()
		
		#filter(EchId=self.params['EchId']).filter(RecordDate__gte=date_tox,RecordDate__lte=date_fromx)
		#NcmEchMonthSum = NcmEchMonthDetails.sum('CpuPercent')
		for i in range(30):
			Days = i + 1
			d1 = NowDateTime + datetime.timedelta(days = -Days)
			#分段执行时段列表
			date_from = datetime.datetime(d1.year,d1.month,d1.day,0,0,0)
			date_to = datetime.datetime(d1.year,d1.month,d1.day,23,59,59)
			
			#定义时间轴日期
			date_Hour = date_from.strftime('%m-%d')
			xdata.append(date_Hour)
			#print NcmEchMonthDetails.count()
			#print type(NcmEchMonthDetails)
			#NcmEchMonthDetail = NcmEchMonthDetails.to_mongo()
			#len(NcmEchMonthDetail)
			#NcmEchMonthDetails.sum('CpuPercent')
			#NcmEchMonthDetails = NcmEchMonthDetails.filter(RecordDate__gte=date_from,RecordDate__lte=date_to).average('CpuPercent')
			#NcmEchMonthDetails=NcmEchMonthDetail.delete()

			#根据时间获取时间段内平均数据百分比
			#NcmEchMonthDetails = NcmEchCpuMonthInfo.objects.filter(EchId=self.params['EchId']).filter(RecordDate__gte=date_from,RecordDate__lte=date_to)
			#PercentSum = NcmEchMonthDetails.sum('CpuPercent')
			NcmEchMonthDetails = NcmEchMonthInfo.objects.filter(MoniterType="CPU").filter(EchId=self.params['EchId']).filter(RecordDate=date_from)
			if NcmEchMonthDetails:
				for NcmEchMonthDetail in NcmEchMonthDetails:
					NcmEchMonthPercent = NcmEchMonthDetail['Percent']
			else:
				NcmEchMonthPercent = 0
			'''
			try:
				NcmEchMonthPercent = float('%0.1f'%(PercentSum/NcmEchMonthDetails.count()))
			except:
				NcmEchMonthPercent = 0
			'''
			ydata.append(NcmEchMonthPercent)

		ydata.reverse()
		xdata.reverse()
		return_data = {
			"ydata" : ydata,
			"xdata" : xdata,
		}
		return_data = json.dumps(return_data)
		return return_data
	def Gain_ECH_MEM_Month_Data(self):
		#获取当前日期及三十天内每天日期
		NowDateTime = datetime.datetime.now()
		ydata = []
		xdata = []
		for i in range(30):
			Days = i + 1
			d1 = NowDateTime + datetime.timedelta(days = -Days)
			#分段执行时段列表
			date_from = datetime.datetime(d1.year,d1.month,d1.day,0,0,0)
			date_to = datetime.datetime(d1.year,d1.month,d1.day,23,59,59)

			#定义时间轴日期
			date_Hour = date_from.strftime('%m-%d')
			xdata.append(date_Hour)

			#根据时间获取时间段内平均数据百分比
			NcmEchMonthDetails = NcmEchMemMonthInfo.objects.filter(EchId=self.params['EchId']).filter(RecordDate__gte=date_from,RecordDate__lte=date_to)
			PercentSum = NcmEchMonthDetails.sum('MemUsaPercent')
			try:
				NcmEchMonthPercent = float('%0.1f'%(PercentSum/NcmEchMonthDetails.count()))
			except:
				NcmEchMonthPercent = 0
			ydata.append(NcmEchMonthPercent)
		ydata.reverse()
		xdata.reverse()
		return_data = {
			"ydata" : ydata,
			"xdata" : xdata,
		}
		return_data = json.dumps(return_data)
		return return_data
	def Gain_ECH_DISK_STRONG_Month_Data(self):
		#获取当前日期及七天内每天日期
		NowDateTime = datetime.datetime.now()
		ydata = []
		xdata = []
		for i in range(30):
			Days = i + 1
			d1 = NowDateTime + datetime.timedelta(days = -Days)
			#分段执行时段列表
			date_from = datetime.datetime(d1.year,d1.month,d1.day,0,0,0)
			date_to = datetime.datetime(d1.year,d1.month,d1.day,23,59,59)

			#定义时间轴日期
			date_Hour = date_from.strftime('%m-%d')
			xdata.append(date_Hour)

			#根据时间获取时间段内平均数据百分比
			NcmEchMonthDetails = NcmEchDiskStrongMonthInfo.objects.filter(EchId=self.params['EchId']).filter(RecordDate__gte=date_from,RecordDate__lte=date_to)
			PercentSum = NcmEchMonthDetails.sum('DiskUsedPercent')
			try:
				NcmEchMonthPercent = float('%0.1f'%(PercentSum/NcmEchMonthDetails.count()))
			except:
				NcmEchMonthPercent = 0
			ydata.append(NcmEchMonthPercent)
		ydata.reverse()
		xdata.reverse()
		return_data = {
			"ydata" : ydata,
			"xdata" : xdata,
		}
		return_data = json.dumps(return_data)
		return return_data