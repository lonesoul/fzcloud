from django.db import models
import datetime
from django.utils import timezone
class users(models.Model):
    uuid = models.CharField(max_length=45)
    UserName = models.CharField(max_length=45)
    Name = models.CharField(max_length=45)
    Password = models.CharField(max_length=32)
    Groups = models.CharField(max_length=45)
    Email = models.CharField(max_length=45)
    Mobile = models.CharField(max_length=11)
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

    
class assets(models.Model):
    uuid = models.CharField(max_length=45)
    HostName = models.CharField(max_length=45)
    HostIp = models.CharField(max_length=45)
    OtherIp = models.CharField(max_length=45)
    MAC = models.CharField(max_length=45)
    ManageAccount = models.CharField(max_length=45)
    Port = models.IntegerField(max_length=45)
    GroupId = models.CharField(max_length=45)
    CPU = models.IntegerField(max_length=45)
    MEM = models.IntegerField(max_length=45)
    Disk = models.IntegerField(max_length=45)
    SystemType = models.CharField(max_length=45)
    SystemVersion = models.CharField(max_length=45)
    HostType = models.CharField(max_length=45)
    OperatEnv = models.CharField(max_length=45)
    HostStatus = models.CharField(max_length=45)
    Status = models.IntegerField(max_length=45)
    Uid = models.CharField(max_length=32)
    CreateTime = models.DateTimeField(auto_now=True)
    class Meta:db_table='x_assets'
class agroups(models.Model):
    uuid = models.CharField(max_length=45)
    Name = models.CharField(max_length=45)
    AssetNum = models.IntegerField()
    Uid = models.CharField(max_length=32)
    CreateTime = models.DateTimeField(auto_now=True)
    class Meta:db_table='x_agroups'
#auto_now_add=True auto_now=True     default=datetime.datetime.now().replace(tzinfo=utc) default=timezone.now()