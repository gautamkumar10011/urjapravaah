from django.db import models
from django.utils import timezone
from django.conf import settings
from emapp.feeder.models import FeederModel

class ScheduleModel(models.Model):
    seq_num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Scheduled")
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add = True)
    dateOn  = models.DateField()
    timeFrom = models.CharField(max_length=16, default="")
    timeTo =  models.CharField(max_length=16, default="")
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    pic_url = models.CharField(max_length=5000)
    feederId = models.ForeignKey(FeederModel, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        ordering = ['name','createdBy']

    def __str__(self):
        return self.name
