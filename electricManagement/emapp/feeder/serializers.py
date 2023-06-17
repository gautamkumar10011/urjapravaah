from rest_framework import serializers
from django.db import transaction
from emapp.feeder.models import FeederModel


class FeederSerializer(serializers.ModelSerializer):
	class Meta:
		model = FeederModel
		fields = '__all__'
