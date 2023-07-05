from django.db import models
from django.utils import timezone
from django.conf import settings


class GroupModel(models.Model):
    seq_num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['name','createdBy']

    def __str__(self):
        return self.name
