from django.db import models
import datetime
from django.utils import timezone
class users(models.Model):
    uuid = models.CharField(max_length=45)
    UserName = models.CharField(max_length=45)
    Name = models.CharField(max_length=45)
    Password = models.CharField(max_length=32)
    Groups = models.IntegerField()
    Email = models.CharField(max_length=45)
    Mobile = models.IntegerField()
    Status = models.IntegerField()
    Power= models.CharField(max_length=32)
    HeadPortrait = models.CharField(max_length=32)
    HostNum = models.IntegerField()
    CreateTime = models.DateTimeField(auto_now_add=True)
    LoginTime = models.DateTimeField(auto_now=True)
    class Meta:db_table='x_users'
class contacts(models.Model):
    uuid = models.CharField(max_length=45)
    Name = models.CharField(max_length=45)
    Email = models.CharField(max_length=45)
    Phone = models.CharField(max_length=32)
    Uid = models.CharField(max_length=32)
    CreateTime = models.DateTimeField(auto_now=True)
    class Meta:db_table='x_contacts'
class cgroups(models.Model):
    uuid = models.CharField(max_length=45)
    Name = models.CharField(max_length=45)
    ContactNum = models.IntegerField()
    Uid = models.CharField(max_length=32)
    CreateTime = models.DateTimeField(auto_now=True)
    class Meta:db_table='x_cgroups'
class c_group(models.Model):
    C_Groupid = models.CharField(max_length=45)
    Contactid = models.CharField(max_length=45)
    Uid = models.CharField(max_length=32)
    CreateTime = models.DateTimeField(auto_now=True)
    class Meta:db_table='x_c_group'    
    
#auto_now_add=True auto_now=True     default=datetime.datetime.now().replace(tzinfo=utc) default=timezone.now()