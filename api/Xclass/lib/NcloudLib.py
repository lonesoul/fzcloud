# -*- coding: utf-8 -*-

"""
Ncloud lib
yun@niuduz.com
"""

import os

from os.path import basename

import time
import datetime

import requests
import logging
import platform
from hashlib import md5
import ctypes 
import sys
import base64
import subprocess
import socket
import json
import random

def date(unixtime, format = '%m/%d/%Y %H:%M'):
	d = datetime.datetime.fromtimestamp(unixtime)
	return d.strftime(format)
def strtotime(timeStr, format = '%Y-%m-%d %H:%M:%S'):
	time_tuple = time.strptime(timeStr, format)
	timestamp = time.mktime(time_tuple)
	return int(timestamp)
def info(str):
	logger = logging.getLogger('JKB')
	FileHandler = logging.FileHandler(getPath()+'log/'+date(time.time(), format = '%Y-%m-%d')+'.log')
	FileHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
	logger.addHandler(FileHandler)
	logger.setLevel(logging.INFO)
	logger.info(str)
	logger.removeHandler(FileHandler)
	FileHandler.close()

def error(str):
	logger = logging.getLogger('JKB')
	FileHandler = logging.FileHandler(getPath()+'log/'+date(time.time(), format = '%Y-%m-%d')+'.log')
	FileHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
	logger.addHandler(FileHandler)
	logger.setLevel(logging.INFO)
	logger.error(str)
	logger.removeHandler(FileHandler)
	FileHandler.close()
def checkPidWin(pid=0):
	cmd='tasklist /FI "PID eq '+str(pid)+'"  /FI "IMAGENAME eq python.exe "'
	returnstr=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
	data = returnstr.stdout.read()
	if len(data) > 150:
		return True
	else :
		return False
def checkPidLinux(pid=0):
	cmd='ps ax |grep '+str(pid)+' |grep python'
	returnstr=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
	data = returnstr.stdout.read()
	if len(data) > 20:
		return True
	else :
		return False
def writePid(pid,pidType):
	pidPath=None
	homePath = ''
	if UsePlatform() == 'Windows' :
		homePath = getPath()
	if pidType=='agent':
		pidPath=homePath+'tmp/agentpid.pid'
	else :
		pidPath=homePath+'tmp/masterpid.pid'
	pid = str(pid)
	pf = open(pidPath,'w')
	pf.write("%s\n" % pid)
	pf.close()
def rmPid(pidType):
	pidPath=None
	homePath = ''
	if UsePlatform() == 'Windows' :
		homePath = getPath()
	if pidType=='agent':
		pidPath=homePath+'tmp/agentpid.pid'
	else :
		pidPath=homePath+'tmp/masterpid.pid'
	pf = open(pidPath,'w')
	pf.write("0")
	pf.close()
def readPid(pidType):
	pidPath=None
	homePath = ''
	if UsePlatform() == 'Windows' :
		homePath = getPath()
		
	if pidType=='agent':
		pidPath=homePath+'tmp/agentpid.pid'
	else :
		pidPath=homePath+'tmp/masterpid.pid'
	if os.path.exists(pidPath):
		pf = open(pidPath,'r')
		pid = int(pf.read().strip())
		if pid ==0 :
			pid =False
		pf.close()
		return pid
	else :
		return 0
def UsePlatform():
	sysstr = platform.system()
	if(sysstr =="Windows"):
		return 'Windows'
	elif(sysstr == "Linux"):
		return 'Linux'
	else:
		return 'Other'
def getPath():
	str=os.path.split(os.path.realpath(__file__))
	str=os.path.split(str[0])
	return str[0]+'/'

def printout(data):
	sys.stderr.write(data+'\n')
	
def getPythonVer():
	var = platform.python_version()
	return var[0]+var[1]+var[2]
def get_mac_address():
	if UsePlatform() == 'Windows':
		mac = os.popen('getmac /NH')
		macaddr = mac.read().split('\n')
		maclist = []
		for a in macaddr:
			n = a.find('-')
			if n != -1:
				a= a.split()[0].lower().replace('-',':')
				maclist.append(a)
		return maclist[-1]
	else:
		import uuid
		node = uuid.getnode()
		mac = uuid.UUID(int = node).hex[-12:]
		return ":".join([mac[e:e+2] for e in range(0,11,2)]).lower()
def estimate_Path(Path):
	status = os.path.exists(Path)
	return status
def estimate_file(filePath):
	status = os.path.exists(filePath)
	return status
def getRandomNum(digit):
	_letter_cases = "abcdefghjkmnpqrstuvwxy" # 小写字母，去除可能干扰的i，l，o，z
	#_upper_cases = _letter_cases.upper() # 大写字母
	_numbers = ''.join(map(str, range(3, 10))) # 数字
	#init_chars = ''.join((_letter_cases, _upper_cases, _numbers))
	init_chars = ''.join((_letter_cases, _numbers))
	c_chars = random.sample(init_chars, digit)
	KeyRandom = ''.join(c_chars)
	return KeyRandom
def HttpRequest(params,ServerIp,port):
	params = json.dumps(params)
	url = 'http://%s:%s/' %(ServerIp,port)

	try:
		r = requests.post(url,data=params)
		return_data =  r.json()
	except:
		return_data = {
			'code':10000,
		}

	return return_data
def md5Encrypt(id):
	import hashlib
	m = hashlib.md5()
	m.update(id)
	return m.hexdigest()
def buildMac():
	mac = [0xfa, 0x16, random.randint(0x00, 0xff),random.randint(0x00, 0xff),random.randint(0x00, 0xff),random.randint(0x00, 0xff)]
	return ':'.join(map(lambda x: "%02x" % x, mac))