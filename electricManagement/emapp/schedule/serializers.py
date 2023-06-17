from rest_framework import serializers
from django.db import transaction
from emapp.schedule.models import ScheduleModel


class ScheduleSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScheduleModel
		fields = '__all__'
