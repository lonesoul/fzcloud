# -*- coding:utf-8 -*-
from mongoengine import *
cennect('test')
class User(Document):
	username = StringField(required=True)
	website = URLField()
	tags = ListField(StringField(max_length=16))
'''
def index(request):
	NowTime = datetime.datetime.now()
	#entry = UserInfo(UserEmail='shengyuan@niuduz.com',PassWord='21232f297a57a5a743894a0e4a801fc3',UserName='',UserMobile=0,UserType=1,VNCPasswd='21232f297a57a5a743894a0e4a801fc3',LoginTime=NowTime)
	#entry.save()
	#p = user.objects(password='admin')
	#p.userName='test'
	#p.save()
	#p = user.objects.get(password='admin')
	#p.password ='aaaa'
	
	
	
	#user.objects.filter(userName='admin').update(password='21232f297a57a5a743894a0e4a801fc3')
	for e in UserInfo.objects.all():
		print e["id"],e["UserEmail"],e["PassWord"]
	res = datetime.datetime.now()
	return HttpResponse(res)
'''
	'''
	user1 = User(
		username = 'Perchouli',
		website = 'http;//dmyz.org',
		tags = ['Web','Django',''JS]
	)
	user1.save()
	Oid = user1.id
	'''