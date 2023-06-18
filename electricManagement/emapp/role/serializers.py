from rest_framework import serializers
from django.db import transaction
from emapp.role.models import UserRoleModel
from emapp.role.models import CRUDModel
from emapp.role.models import ComponetName

NONE = 0
OPERATION_DICT = {"None":0,
          "Create": 8,
          "Read": 4,
          "Update": 2,
          "Delete": 1,
          "ReadCreate":12,
          "ReadUpdate": 6,
          "ReadDelete": 5,
          "CreateReadUpdate": 14,
          "All": 15,
          "CreateDelete":13,
          "CreateUpdate":14,
          "UpdateDelete":7}


class UserRoleSerializer(serializers.ModelSerializer):
	feeder = serializers.SerializerMethodField('get_feeder')
	def get_feeder(self, obj):
		if obj.feeder:
			return OPERATION_DICT[obj.feeder.operations]
		return NONE	
	station = serializers.SerializerMethodField('get_station')
	def get_station(self, obj):
		if obj.station:
			return OPERATION_DICT[obj.station.operations]
		return NONE
	feederStation = serializers.SerializerMethodField('get_feeder_station')
	def get_feeder_station(self, obj):
		if obj.feederStation:
			return OPERATION_DICT[obj.feederStation.operations]
		return NONE			
	control_panel = serializers.SerializerMethodField('get_control_panel')
	def get_control_panel(self, obj):
		if obj.control_panel:
			return OPERATION_DICT[obj.control_panel.operations]
		return NONE		

	class Meta:
		model = UserRoleModel
		fields = ("seq_num",
					"name",
					"createdBy",
					"createdAt",
					"updatedAt",
					"feeder",
					"station",
					"feederStation",
					"control_panel")

class CRUDSerializer(serializers.ModelSerializer):
	class Meta:
		model = CRUDModel
		fields = '__all__'


class ComponetNameSerializer(serializers.ModelSerializer):
	class Meta:
		model = ComponetName
		fields = ["name","displayName"]	
