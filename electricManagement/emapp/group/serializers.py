from rest_framework import serializers
from django.db import transaction
from emapp.group.models import GroupModel


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = GroupModel
		fields = '__all__'
