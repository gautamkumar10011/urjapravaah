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
from emapp.station.models import StationModel
from emapp.station.serializers import StationSerializer
from emapp.role import ROLE
from emapp.feeder.models import FeederModel
from emapp.feeder.serializers import FeederSerializer
from emapp.permission.models import UserFeeder


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_station(request):
    if not ROLE.isValidOperation(ROLE.KEY_STATION, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num =  request.GET['seq_num']
        data = StationModel.objects.get(seq_num=seq_num)
        result = StationSerializer(data).data
        result['username'] = User.objects.get(id=result['createdBy']).username
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_feeder_by_station_id(request):
    if not ROLE.isValidOperation(ROLE.KEY_STATION, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = User.objects.get(username=request.user.username)
        seq_num =  request.GET['seq_num']
        feeders = FeederModel.objects.filter(stationId=seq_num)
        records = FeederModel.objects.none()
        for feeder in feeders:
            if UserFeeder.objects.filter(userId=user,feederId=feeder).exists():
                records |= FeederModel.objects.filter(seq_num=feeder.seq_num)

        result = list()
        for record in records:
            serialized_record = FeederSerializer(record).data
            serialized_record['username'] = User.objects.get(id=serialized_record['createdBy']).username
            serialized_record['station'] = StationModel.objects.get(seq_num=seq_num).name
            result.append(serialized_record)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_stations(request):
    if not ROLE.isValidOperation(ROLE.KEY_STATION, ROLE.KEY_READ, request.user.username):
        return Respnse(status=status.HTTP_401_UNAUTHORIZED)
    user = User.objects.get(username=request.user.username)
    userFeeders = UserFeeder.objects.filter(userId=user)
    result = list()
    feederMap = dict()
    for userFeeder in userFeeders:
        if userFeeder.feederId.stationId not in feederMap:
            result.append(
                userFeeder.feederId.stationId
            )
            feederMap[userFeeder.feederId.stationId] = True

    allRecords = StationModel.objects.none()
    for stationId in result:
        allRecords |= StationModel.objects.filter(seq_num=stationId.seq_num)
    
    result = list()
    for record in allRecords:
        serialized_record = StationSerializer(record).data
        serialized_record['username'] = User.objects.get(id = serialized_record['createdBy']).username       
        result.append(serialized_record)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_station(request):
    if not ROLE.isValidOperation(ROLE.KEY_STATION, ROLE.KEY_CREATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        saved_data = StationModel.objects.create(createdBy=user, **payload)
        result = StationSerializer(StationModel.objects.get(seq_num=saved_data.seq_num)).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def update_station(request):
    if not ROLE.isValidOperation(ROLE.KEY_STATION, ROLE.KEY_UPDATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = json.loads(request.body.decode())
        StationModel.objects.filter(seq_num=payload['seq_num']).update( **payload)
        result = StationSerializer(StationModel.objects.get(seq_num=payload['seq_num'])).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_station(request):
    if not ROLE.isValidOperation(ROLE.KEY_STATION, ROLE.KEY_DELETE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num = request.GET['seq_num']
        StationModel.objects.filter(seq_num=seq_num).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


