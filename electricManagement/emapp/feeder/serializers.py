from rest_framework import serializers
from django.db import transaction
from emapp.feeder.models import FeederModel,StationModel


class FeederSerializer(serializers.ModelSerializer):
    station = serializers.CharField(source='stationId.name')

    class Meta:
        model = FeederModel
        fields = '__all__'
