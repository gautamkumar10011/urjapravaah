from rest_framework import serializers
from django.db import transaction
from emapp.permission.models import UserFeeder
from emapp.permission.models import GroupFeeder


class UserFeederSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserFeeder
		fields = '__all__'


class GroupFeederSerializer(serializers.ModelSerializer):
	class Meta:
		model = GroupFeeder
		fields = '__all__'		