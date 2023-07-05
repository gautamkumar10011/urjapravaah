from django.db import models
from django.utils import timezone
from django.conf import settings

OPERATIONS = (("None","None"),
              ("Create","Create"),
              ("Read","Read"),
              ("Update","Update"),
              ("Delete","Delete"),
              ("ReadCreate","ReadCreate"),
              ("ReadUpdate","ReadUpdate"),
              ("ReadDelete","ReadDelete"),
              ("CreateReadUpdate","CreateReadUpdate"),
              ("All","All"))

class CRUDModel(models.Model):
    seq_num = models.AutoField(primary_key=True)
    operations = models.CharField(max_length=50,unique=True)
    value = models.IntegerField(default=0) 


    class Meta:
        ordering = ['operations',]

    def __str__(self):
        return self.operations


class UserRoleModel(models.Model):
    seq_num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now_add = True)
    feeder = models.ForeignKey(CRUDModel, on_delete=models.SET_NULL,related_name='feeder', null=True, blank=True) 
    station = models.ForeignKey(CRUDModel, on_delete=models.SET_NULL,related_name='station', null=True, blank=True)
    schedule = models.ForeignKey(CRUDModel, on_delete=models.SET_NULL,related_name='schedule', null=True, blank=True)
    role = models.ForeignKey(CRUDModel, on_delete=models.SET_NULL,related_name='role', null=True, blank=True)
    urjauser = models.ForeignKey(CRUDModel, on_delete=models.SET_NULL,related_name='urjauser', null=True, blank=True)
    control_panel = models.ForeignKey(CRUDModel, on_delete=models.SET_NULL,related_name='control_panel', null=True, blank=True)
    group = models.ForeignKey(CRUDModel, on_delete=models.SET_NULL,related_name='group', null=True, blank=True)
    views = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['name','createdBy']

    def __str__(self):
        return str(self.name)

class ComponetName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,unique=True)
    displayName = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)
