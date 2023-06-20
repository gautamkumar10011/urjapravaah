from django.db import models
from django.utils import timezone
from django.conf import settings
from emapp.station.models import StationModel


class FeederModel(models.Model):
    seq_num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stationId = models.ForeignKey(StationModel, on_delete=models.CASCADE, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now_add = True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    class Meta:
        ordering = ['name','createdBy']

    def __str__(self):
        return self.name
