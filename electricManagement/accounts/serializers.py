from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("id","last_login","username","first_name", 'is_superuser',
					"last_name","is_active","is_staff","readonly","language",
				    "email","phone","roleId","is_public", 'play_device')