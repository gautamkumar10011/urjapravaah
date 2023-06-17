from django.db import models
from django.utils import timezone
from django.conf import settings
from emapp.feeder.models import FeederModel
from emapp.station.models import StationModel

class FeederStationModel(models.Model):
    feederId = models.ForeignKey(FeederModel, on_delete=models.CASCADE)
    stationId = models.ForeignKey(StationModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['stationId',]
