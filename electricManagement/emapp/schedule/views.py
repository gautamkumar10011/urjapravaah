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


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_schedule(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULLE, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num =  request.GET['seq_num']
        result = ScheduleSerializer(ScheduleModel.objects.get(seq_num=seq_num)).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_schedules(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULLE, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    result = ScheduleSerializer(ScheduleModel.objects.all(),many=True).data
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_schedule(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULLE, ROLE.KEY_CREATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        saved_data = ScheduleModel.objects.create(createdBy=user, **payload)
        result = ScheduleSerializer(ScheduleModel.objects.get(seq_num=saved_data.seq_num)).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def update_schedule(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULLE, ROLE.KEY_UPDATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = json.loads(request.body.decode())
        if 'createdBy' in payload: del payload['createdBy']
        ScheduleModel.objects.filter(seq_num=payload['seq_num']).update(**payload)
        result = ScheduleSerializer(ScheduleModel.objects.get(seq_num=payload['seq_num'])).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_schedule(request):
    if not ROLE.isValidOperation(ROLE.KEY_SCHEDULLE, ROLE.KEY_DELETE, request.user.username):
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
    result = ScheduleModel.objects.filter(dateOn=dateOn)
    finalResult = ScheduleSerializer(result, many=True).data
    return Response(finalResult, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_schedule_date_range(request):
    dateFrom = request.GET.get('dateFrom')
    dateTo = request.GET.get('dateTo')
    result = ScheduleModel.objects.filter(dateOn__range=[dateFrom,dateTo])
    finalResult = ScheduleSerializer(result, many=True).data
    return Response(finalResult, status=status.HTTP_200_OK)