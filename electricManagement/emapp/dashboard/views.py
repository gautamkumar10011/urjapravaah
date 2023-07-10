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
from django.db.models import Q

DAYS_INTERVAL=15

@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        userFeeders = UserFeeder.objects.filter(userId=user)
        totalFeeder, totatStation = get_total_station(user, userFeeders)
        totalSchedule = get_total_schedule(user, userFeeders)
        totalPending = get_total_scheduled(user, userFeeders)
        totalAcknowledged = totalSchedule - totalPending
        graphData = get_graph_data1(user, userFeeders)
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
        result['graphData'] = graphData
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_404_NOT_FOUND)


def get_total_station(user, UserFeeders):
    user_feeders = UserFeeder.objects.filter(userId=user).values_list('feederId__stationId', flat=True)
    unique_stations = set(user_feeders)
    return len(user_feeders), len(unique_stations)

def get_total_schedule(user, userFeeders):
    records = ScheduleModel.objects.filter(
        dateOn__gte=datetime.now(),
        feederId__in=[userFeeder.feederId for userFeeder in userFeeders]
    )
    return records.count()

def get_total_scheduled(user, userFeeders):
    records = ScheduleModel.objects.filter(
        Q(dateOn__gte=datetime.now()) & Q(feederId__in=[userFeeder.feederId for userFeeder in userFeeders]) & Q(status="Scheduled")
    )
    return records.count()

def get_graph_data(user, userFeeders):
    result = list()
    records = ScheduleModel.objects.none()
    for i in range(DAYS_INTERVAL):
        total_time = 0
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

def get_graph_data1(user, userFeeders):
    result = []
    user_feeders = userFeeders
    records = ScheduleModel.objects.none()

    for i in range(DAYS_INTERVAL):
        date_on = datetime.today() - timedelta(days=i)
        records = ScheduleModel.objects.filter(dateOn=date_on, feederId__in=user_feeders.values_list('feederId', flat=True))

        total_time = 0
        for record in records:
            time_from = (HOURS[record.timeFrom[0:2]] * 60 + MINS[record.timeFrom[3:]])
            time_to = (HOURS[record.timeTo[0:2]] * 60 + MINS[record.timeTo[3:]])
            total_time += (time_to - time_from) / 60

        result.append({
            "day": date_on.strftime('%Y-%m-%d'),
            "total_time": total_time
        })
    return result

def get_graph_data2(user, userFeeders):
    result = []
    fifteen_days_ago = date.today() - timedelta(days=15)
    schedules = ScheduleModel.objects.filter(dateOn__gte=fifteen_days_ago, feederId__in=userFeeders)

