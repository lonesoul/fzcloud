# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os
#导出数据结构模块
from api.models import *
#from api.ManagerEch import *
#导入命令执行模块

import commands
import socket

def valid_ip(address):
	try: 
		socket.inet_aton(address)
		return True
	except:
		return False

#获取计算LBId

def GetLbId():
	LbList = LbInfo.objects.all().order_by('-CreateTime')[0:1]
	if LbList:
		for Lb in LbList:
			LbRawId = Lb.LbId
		LbRawNum = LbRawId.split('-')
		#生成LbId
		LbNum = int(LbRawNum[1]) + 1
		#生成LBID
		LbId = 'lb-%s' % LbNum
	else:
		LbNum = 1000001
		LbId = 'lb-%s' % LbNum
	return LbId
def GetDoubletLvsCfg(parame):
	keepalivedM = """
		vrrp_instance VI_%s {
			state MASTER
			interface eth1
			virtual_router_id %s
			priority 100
			advert_int 1
			authentication {
				auth_type PASS
				auth_pass 1111
			}
			virtual_ipaddress {
				%s
			}
		}
		vrrp_instance VI_%s {
			state MASTER
			interface eth2
			virtual_router_id %s
			priority 100
			advert_int 1
			authentication {
				auth_type PASS
				auth_pass 1111
			}
			virtual_ipaddress {
				%s
			}
		}
	""" % (parame['TVrrpNum'],parame['TVrrpNum'],parame['Tip'],parame['UVrrpNum'],parame['UVrrpNum'],parame['Uip'])
	keepalivedB = """
		vrrp_instance VI_%s {
			state BACKUP
			interface eth1
			virtual_router_id %s
			priority 99
			advert_int 1
			authentication {
				auth_type PASS
				auth_pass 1111
			}
			virtual_ipaddress {
				%s
			}
		}
		vrrp_instance VI_%s {
			state BACKUP
			interface eth2
			virtual_router_id %s
			priority 99
			advert_int 1
			authentication {
				auth_type PASS
				auth_pass 1111
			}
			virtual_ipaddress {
				%s
			}
		}
		""" % (parame['TVrrpNum'],parame['TVrrpNum'],parame['Tip'],parame['UVrrpNum'],parame['UVrrpNum'],parame['Uip'])
	LBroute = ['ip rule add from %s lookup telecom' % parame['Tip'],'ip rule add from %s lookup unicom' % parame['Uip']]
	return_data = {
		'keepalivedM':keepalivedM,
		'keepalivedB' : keepalivedB,
		'LBroute' : LBroute,
	}
	return return_data
def GetDoubletCreateLBCfg(parame):
	LBservers = []
	for NLBHandle in parame:
		LBserver = """
	server {
			listen	%s:80;
			return 200 "200";
		}
	""" % (NLBHandle['LbsIp'])
		LBservers.append(LBserver)
	LBservers = ''.join(LBservers)
	return_data = {
		'LBserver' : LBservers,
	}
	return return_data
def GetDoubletLvsVirtualCfg(parame):
	real_servers = []
	for RealIp in parame['RealIps']:
		real_server = '''
	real_server %s %s {
		weight 100
		TCP_CHECK {
			connect_timeout 3
			nb_get_retry 3
			delay_before_retry 3
		}
	}''' % (RealIp,parame['listener_port'])
		real_servers.append(real_server)
	real_servers = ''.join(real_servers)
	LVSVirtualInfo = """
virtual_server %s %s {
	delay_loop 6
	lb_algo rr
	lb_kind NAT
	persistence_timeout 50
	protocol TCP
	%s
}
virtual_server %s %s {
	delay_loop 6
	lb_algo rr
	lb_kind NAT
	persistence_timeout 50
	protocol TCP
	%s
}
""" % (parame['Tip'],parame['listener_port'],real_servers,parame['Uip'],parame['listener_port'],real_servers)
	
	return_data = {
		'LVSVirtualInfo' : LVSVirtualInfo,
	}
	return return_data
def HandleVisitPlace(params):

	visit_place_val = params['listeners'][0]['visit_place_val']
	VisitPlaceList =''
	if visit_place_val == '':
		return_data = {
			'VisitPlaceFruit' : 1,
			'VisitPlaceList' : '',
		}
	else:
		visit_place = visit_place_val.split(';\n')
		if len(visit_place) == 1:
			visit_place = visit_place_val.split(';')
			if len(visit_place) == 2:
				if visit_place[1] == '':
					print visit_place[0]
					validStatus = valid_ip(visit_place[0])
					if validStatus:
						VisitPlaceFruit = 1
						VisitPlaceList = """
							allow %s;
							deny all;
						""" % visit_place[0]
					else:
						VisitPlaceFruit = 0
						VisitPlaceList = ''
				else:
					VisitPlaceFruit = 0
					VisitPlaceList = ''
			else:
				VisitPlaceFruit = 0
				VisitPlaceList = ''
			return_data = {
					'VisitPlaceFruit' : VisitPlaceFruit,
					'VisitPlaceList' : VisitPlaceList,
			}
		else:
			for i,val in enumerate(visit_place):
				if i == len(visit_place) - 1:
					visit_placeVal = val.split(';')
					if len(visit_placeVal) == 2:
						if visit_placeVal[1] == '':
							validStatus = valid_ip(visit_placeVal[0])
							print validStatus
							if validStatus:
								VisitPlaceFruit = 1
								VisitPlaceList += """
								allow %s;
								deny all;""" % visit_placeVal[0]
							else:
								VisitPlaceFruit = 0
								VisitPlaceList = ''
								break
						else:
							VisitPlaceFruit = 0
							VisitPlaceList = ''
							break
					else:
						VisitPlaceFruit = 0
						VisitPlaceList = ''
						break
				else:
					validStatus = valid_ip(val)
					if validStatus:
						VisitPlaceFruit = 1
						VisitPlaceList += """
						allow %s;\n""" % val
					else:
						VisitPlaceFruit = 0
						VisitPlaceList = ''
						break
			return_data = {
				'VisitPlaceFruit' : VisitPlaceFruit,
				'VisitPlaceList' : VisitPlaceList,
			}
	return return_data