import django
django.setup()
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
from emapp.schedule.models import ScheduleModel
from emapp.schedule.serializers import ScheduleSerializer
from emapp.role import ROLE
from emapp.feeder.models import FeederModel
from emapp.sms_n_notification.send_email import send_email_to_station
from emapp.sms_n_notification.fcm_manager import send_notification
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Process
from emapp.group.models import GroupModel
from emapp.permission.models import GroupFeeder

@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_schedule(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULE, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num =  request.GET['seq_num']
        data = ScheduleModel.objects.get(seq_num=seq_num)
        result = ScheduleSerializer(data).data
        result['feeder'] = None
        if FeederModel.objects.filter(seq_num=result['feederId']).exists():
            result['feederId'] = FeederModel.objects.get(seq_num=result['feederId']).name
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_schedules(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULE, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    records = ScheduleModel.objects.all()
    result = list()
    for record in records:
        serialized_record = ScheduleSerializer(record).data
        serialized_record['feeder'] = None
        if FeederModel.objects.filter(seq_num=serialized_record['feederId']).exists():
            serialized_record['feederId'] = FeederModel.objects.get(seq_num=serialized_record['feederId']).name        
        result.append(serialized_record)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_schedule(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULE, ROLE.KEY_CREATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        feeder_id = payload['feederId']
        feeder = FeederModel.objects.get(seq_num=feeder_id)
        if 'feederId' in payload: del payload['feederId']
        saved_data = ScheduleModel.objects.create(createdBy=user, feederId= feeder, **payload)
        result = ScheduleSerializer(ScheduleModel.objects.get(seq_num=saved_data.seq_num)).data

        bgprocess1 = Process(target=send_email_to_station, args=( feeder, payload,))
        bgprocess1.start()
        bgprocess = Process(target=send_notification, args=( feeder, payload, saved_data))
        bgprocess.start()
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def schedule_group(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULE, ROLE.KEY_CREATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)    
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        group = GroupModel.objects.get(seq_num=payload['groupId'])
        groupFeeders = GroupFeeder.objects.filter(groupId=group)
        del payload['groupId']
        for groupFeeder in groupFeeders:
            saved_data = ScheduleModel.objects.create(createdBy=user, feederId= groupFeeder.feederId, **payload)
            bgprocess1 = Process(target=send_email_to_station, args=( groupFeeder.feederId, payload,))
            bgprocess = Process(target=send_notification, args=( groupFeeder.feederId, payload, saved_data))
            bgprocess1.start()
            bgprocess.start()            
        return Response(status=status.HTTP_201_CREATED) 
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def update_schedule(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULE, ROLE.KEY_UPDATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = json.loads(request.body.decode())
        if 'createdBy' in payload: del payload['createdBy']
        feeder_id = payload['feederId']
        feeder = None 
        if FeederModel.objects.filter(seq_num=feeder_id).exist():
            feeder = FeederModel.objects.get(seq_num=feeder_id)
        if 'feederId' in payload: del payload['feederId']        
        ScheduleModel.objects.filter(seq_num=payload['seq_num']).update(feederId=feeder, **payload)
        result = ScheduleSerializer(ScheduleModel.objects.get(seq_num=payload['seq_num'])).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_schedule(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULE, ROLE.KEY_DELETE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num = request.GET['seq_num']
        ScheduleModel.objects.filter(seq_num=seq_num).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"errMessage": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_schedule_by_date(request):
    dateOn = request.GET.get('dateOn')
    scheduleType = request.GET.get('scheduleType')
    if scheduleType == "Scheduled":
        records = ScheduleModel.objects.filter(status=scheduleType, dateOn=dateOn)
    elif scheduleType == "Acknowledged":
        records = ScheduleModel.objects.filter(status=scheduleType, dateOn=dateOn)
    else:
        records = ScheduleModel.objects.filter(dateOn=dateOn)
    
    result = list()
    for record in records:
        serialized_record = ScheduleSerializer(record).data
        serialized_record['feeder'] = None
        if FeederModel.objects.filter(seq_num=serialized_record['feederId']).exists():
            serialized_record['feeder'] = FeederModel.objects.get(seq_num=serialized_record['feederId']).name
        result.append(serialized_record)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_schedule_date_range(request):
    dateFrom = request.GET.get('dateFrom')
    dateTo = request.GET.get('dateTo')
    scheduleType = request.GET.get('scheduleType')
    if scheduleType == "Scheduled":
        records = ScheduleModel.objects.filter(status=scheduleType, dateOn__range=[dateFrom,dateTo])
    elif scheduleType == "Acknowledged":
        records = ScheduleModel.objects.filter(status=scheduleType, dateOn__range=[dateFrom,dateTo])
    else:    
        records = ScheduleModel.objects.filter(dateOn__range=[dateFrom,dateTo])
    result = list()
    for record in records:
        serialized_record = ScheduleSerializer(record).data
        serialized_record['feeder'] = None
        if FeederModel.objects.filter(seq_num=serialized_record['feederId']).exists():
            serialized_record['feeder'] = FeederModel.objects.get(seq_num=serialized_record['feederId']).name
        result.append(serialized_record)    
    return Response(result, status=status.HTTP_200_OK)

