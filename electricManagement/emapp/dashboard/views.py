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
from emapp.permission.models import UserFeeder
from datetime import datetime, timedelta
from emapp.dashboard.hoursMinsConstants import HOURS
from emapp.dashboard.hoursMinsConstants import MINS

DAYS_INTERVAAL=7

@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        totalFeeder = UserFeeder.objects.filter(userId=user).count()
        totatStation = get_total_station(user)
        totalSchedule = get_total_schedule(user)
        totalPending = get_total_scheduled(user)
        totalAcknowledged = totalSchedule - totalPending
        #graphData = get_graph_data(user)
        # [{"day":"2023-06-08", "total_time":4},
        # {"day":"2023-06-9", "total_time": 3},
        # {"day":"2023-06-10", "total_time": 4},
        # {"day":"2023-06-11", "total_time": 6},
        # {"day":"2023-06-12", "total_time": 8},
        # {"day":"2023-06-13", "total_time": 12},
        # {"day":"2023-06-14", "total_time": 11},
        # {"day":"2023-06-15", "total_time": 21},
        # {"day":"2023-06-16", "total_time": 12},
        # {"day":"2023-06-17", "total_time": 6},
        # {"day":"2023-06-18", "total_time": 9},
        # {"day":"2023-06-19", "total_time": 3},
        # {"day":"2023-06-20", "total_time": 9},
        # {"day":"2023-06-21", "total_time": 3},
        # {"day":"2023-06-22", "total_time": 9}]
        result = dict()
        result['totatStation'] = totatStation
        result['totalFeeder'] = totalFeeder
        result['totalSchedule'] = totalSchedule
        result['totalPending'] = totalPending
        result['totalAcknowledged'] = totalAcknowledged
        result['graphData'] = {}#graphData
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_404_NOT_FOUND)


def get_total_station(user):
    userFeeders = UserFeeder.objects.filter(userId=user)
    result = list()
    feederMap = dict()
    for userFeeder in userFeeders:
        if userFeeder.feederId.stationId not in feederMap:
            result.append(
                userFeeder.feederId.stationId
            )
            feederMap[userFeeder.feederId.stationId] = True
    return len(result)


def get_total_schedule(user):
    userFeeders = UserFeeder.objects.filter(userId=user)
    records = ScheduleModel.objects.none()
    for userFeeder in userFeeders:
        records |= ScheduleModel.objects.filter(dateOn__gte=datetime.now(), feederId=userFeeder.feederId)
    return records.count()

def get_total_scheduled(user):
    userFeeders = UserFeeder.objects.filter(userId=user)
    records = ScheduleModel.objects.none()
    for userFeeder in userFeeders:
        records |= ScheduleModel.objects.filter(dateOn__gte=datetime.now(), feederId=userFeeder.feederId, status="Scheduled")
    return records.count()

def get_graph_data(user):
    result = list()
    userFeeders = UserFeeder.objects.filter(userId=user)
    records = ScheduleModel.objects.none()
    for i in range(DAYS_INTERVAAL):
        for userFeeder in userFeeders:
            records |= ScheduleModel.objects.filter(dateOn=datetime.today() - timedelta(days=i), feederId=userFeeder.feederId)
        total_time = 0
        for record in records:
            total_time += ((HOURS[record.timeTo[0:2]]*60 + MINS[record.timeTo[3:]]) - (HOURS[record.timeFrom[0:2]]*60 + MINS[record.timeFrom[3:]]))/60
            result.append({
                "day": (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d'),
                "total_time": total_time
            })
        records = ScheduleModel.objects.none()
    return result
