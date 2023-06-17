from rest_framework import serializers
from django.db import transaction
from emapp.station.models import StationModel


class StationSerializer(serializers.ModelSerializer):
	class Meta:
		model = StationModel
		fields = '__all__'
