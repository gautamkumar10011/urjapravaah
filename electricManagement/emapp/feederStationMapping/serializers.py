from rest_framework import serializers
from django.db import transaction
from emapp.feederStationMapping.models import FeederStationModel


class FeederStationSerializer(serializers.ModelSerializer):
	class Meta:
		model = FeederStationModel
		fields = '__all__'
