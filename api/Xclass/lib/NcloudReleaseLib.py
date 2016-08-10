# coding=utf-8

#导出常用模块
import datetime,json,md5,sys,os
#导出数据结构模块
from api.models import *
#from api.ManagerEch import *
#导入命令执行模块

import commands
#测试环境FTP 地址、用户名 密码
TestIp = '101.231.52.214'
ReadyIp = '11.11.11.12'
def TestCodeToNCloud(Data,params):
	exec_cmd = "wget -c -q -r -nH -l20 -P /release/%s/%s --cut-dirs=2 ftp://dev:123QWEasdZXC@%s/%s/%s" % (Data['UserId'],params['releaseDomain'],TestIp,params['releaseComputer'],params['releaseDomain'])
	cmd_status,result = commands.getstatusoutput(exec_cmd)
	return cmd_status
def CompressedReleaseCode(Data,params,version_time,releaseDomain):
	try:
		if params['readytype']:
			pass
		cmd_status,result = commands.getstatusoutput("mkdir /release/%s/releaseLine" % Data['UserId'])
		if params['config'] == 1:
			exec_cmd = 'rm -rf /release/%s/%s/*eb.config' % (Data['UserId'],releaseDomain)
			cmd_status,result = commands.getstatusoutput(exec_cmd)
		exec_cmd = "zip -q -r /release/%s/releaseLine/%s_%s.zip /release/%s/%s" % (Data['UserId'],releaseDomain,version_time,Data['UserId'],releaseDomain)
		cmd_status,result = commands.getstatusoutput(exec_cmd)
		exec_cmdrm = 'rm -rf /release/%s/%s' % (Data['UserId'],releaseDomain)
		cmd_status,result = commands.getstatusoutput(exec_cmdrm)
	except:
		cmd_status,result = commands.getstatusoutput("mkdir /release/%s/releaseReady" % Data['UserId'])
		if params['config'] == 1:
			exec_cmd = 'rm -rf /release/%s/%s/*eb.config' % (Data['UserId'],params['releaseDomain'])
			cmd_status,result = commands.getstatusoutput(exec_cmd)
		exec_cmd = "zip -q -r /release/%s/releaseReady/%s_%s.zip /release/%s/%s" % (Data['UserId'],params['releaseDomain'],version_time,Data['UserId'],params['releaseDomain'])
		cmd_status,result = commands.getstatusoutput(exec_cmd)
		exec_cmdrm = 'rm -rf /release/%s/%s' % (Data['UserId'],params['releaseDomain'])
		cmd_status,result = commands.getstatusoutput(exec_cmdrm)
	return cmd_status
def UpReadyReleaseCode(Data,params):
	if params['config'] == 1:
		exec_cmd = 'rm -rf /release/%s/%s/*eb.config' % (Data['UserId'],params['releaseDomain'])
		cmd_status,result = commands.getstatusoutput(exec_cmd)
	else:
		cmd_status = 0
	if cmd_status == 0:
		exec_cmdleft = 'lftp -u ftpready,\'123QWEasdZXC\' -e "set net:reconnect-interval-base 0;set file:charset GBK;mirror -R /release/%s/%s /%s/%s;exit" 11.11.11.12' % (Data['UserId'],params['releaseDomain'],params['releaseComputer'],params['releaseDomain'])
		#'lftp -u dev,\'123QWEasdZXC\' -e "set net:reconnect-interval-base 0;set file:charset GBK;mirror -R /release/%s/%s /test/%s;exit" 192.168.1.220' % (Data['UserId'],params['releaseDomain'],params['releaseDomain'])
		#'lftp -u ftpready,\'123QWEasdZXC\' -e "set net:reconnect-interval-base 0;set file:charset GBK;mirror -R /release/%s/%s /%s/%s;exit" 11.11.0.12' % (Data['UserId'],params['releaseDomain'],params['releaseComputer'],params['releaseDomain'])
		cmd_status,result = commands.getstatusoutput(exec_cmdleft)
		if cmd_status == 0:
			exec_cmdrm = 'rm -rf /release/%s/%s' % (Data['UserId'],params['releaseDomain'])
			cmd_status,result = commands.getstatusoutput(exec_cmdrm)
	return cmd_status
def ReadyCodeToNCloud(Data,params,releaseDomain):
	#从预发布环境获取代码到云平台
	exec_cmd = "wget -c -q -r -nH -l20 -P /release/%s/%s --cut-dirs=2 ftp://ftpready:123QWEasdZXC@%s/%s/%s" % (Data['UserId'],releaseDomain,ReadyIp,params['releaseComputer'],params['releaseDomain'])
	print exec_cmd
	cmd_status,result = commands.getstatusoutput(exec_cmd)
	print result
	return cmd_status
def UpLineReleaseCode(Data,params,EchIp):
	if params['config'] == 1:
		exec_cmd = 'rm -rf /release/%s/%s/*eb.config' % (Data['UserId'],params['releaseDomain'])
		cmd_status,result = commands.getstatusoutput(exec_cmd)
	else:
		cmd_status = 0
	if cmd_status == 0:
		exec_cmdleft = 'lftp -u %s,\'%s\' -e "set net:reconnect-interval-base 0;set file:charset GBK;mirror -R /release/%s/%s /%s;exit" %s' % (params['ftpuser'],params['ftppwd'],Data['UserId'],params['releaseDomain'],params['releaseDomain'],EchIp)
		#'lftp -u %s,\'%s\' -e "set net:reconnect-interval-base 0;set file:charset GBK;mirror -R /release/%s/%s /%s/%s;exit" 11.11.0.12' % (Data['UserId'],params['releaseDomain'],params['releaseComputer'],params['releaseDomain'])
		cmd_status,result = commands.getstatusoutput(exec_cmdleft)
		if cmd_status == 0:
			exec_cmdrm = 'rm -rf /release/%s/%s' % (Data['UserId'],params['releaseDomain'])
			cmd_status,result = commands.getstatusoutput(exec_cmdrm)
	return cmd_status