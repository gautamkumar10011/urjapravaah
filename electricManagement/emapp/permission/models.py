from django.db import models
from django.utils import timezone
from django.conf import settings
from emapp.feeder.models import FeederModel


class UserFeeder(models.Model):
    feeder = models.ForeignKey(FeederModel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

    def __str__(self):
        return str(self.user) + "-" + str(self.device)
