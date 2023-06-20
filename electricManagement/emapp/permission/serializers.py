from rest_framework import serializers
from django.db import transaction
from emapp.permission.models import UserFeeder


class UserFeederSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserFeeder
		fields = '__all__'