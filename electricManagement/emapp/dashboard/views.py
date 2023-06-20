import json
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
from accounts.models import User
from emapp.feeder.models import FeederModel
from emapp.station.models import StationModel
from emapp.schedule.models import ScheduleModel


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    try:
        totatStation = StationModel.objects.all().count()
        totalFeeder = FeederModel.objects.all().count()
        totalScheculde = ScheduleModel.objects.all().count()
        totalPending = ScheduleModel.objects.filter(status="Pending").count()
        totalAcknowledged = ScheduleModel.objects.filter(status="Acknowledged").count()
        graphData = [{"day":"2023-06-08", "total_time":4},
        {"day":"2023-06-9", "total_time": 3},
        {"day":"2023-06-10", "total_time": 4},
        {"day":"2023-06-11", "total_time": 6},
        {"day":"2023-06-12", "total_time": 8},
        {"day":"2023-06-13", "total_time": 12},
        {"day":"2023-06-14", "total_time": 11},
        {"day":"2023-06-15", "total_time": 21},
        {"day":"2023-06-16", "total_time": 12},
        {"day":"2023-06-17", "total_time": 6},
        {"day":"2023-06-18", "total_time": 9},
        {"day":"2023-06-19", "total_time": 3},
        {"day":"2023-06-20", "total_time": 9},
        {"day":"2023-06-21", "total_time": 3},
        {"day":"2023-06-22", "total_time": 9}]
        result = dict()
        result['totatStation'] = totatStation
        result['totalFeeder'] = totalFeeder
        result['totalScheculde'] = totalScheculde
        result['totalPending'] = totalPending
        result['totalAcknowledged'] = totalAcknowledged
        result['graphData'] = graphData
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_404_NOT_FOUND)