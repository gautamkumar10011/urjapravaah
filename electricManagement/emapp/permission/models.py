from django.db import models
from django.utils import timezone
from django.conf import settings
from emapp.feeder.models import FeederModel
from emapp.group.models import GroupModel


class UserFeeder(models.Model):
    feederId = models.ForeignKey(FeederModel, on_delete=models.CASCADE)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

    def __str__(self):
        return str(self.userId) + "-" + str(self.feederId)


class GroupFeeder(models.Model):
    feederId = models.ForeignKey(FeederModel, on_delete=models.CASCADE)
    groupId = models.ForeignKey(GroupModel, on_delete=models.CASCADE) 

    def __str__(self):
        return str(self.groupId) + "-" + str(self.feederId)
