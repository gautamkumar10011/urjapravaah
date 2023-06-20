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
from emapp.feeder.serializers import FeederSerializer
from emapp.role import ROLE
from emapp.station.models import StationModel


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_feeder(request):
    if not ROLE.isValidOperation(ROLE.KEY_FEEDER, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        feeder_id =  request.GET['seq_num']
        data = FeederModel.objects.get(seq_num=feeder_id)
        result = FeederSerializer(data).data
        result['station'] = None
        if StationModel.objects.filter(seq_num=result['stationId']).exists():
            result['station'] = StationModel.objects.get(seq_num=result['stationId']).name
        result['username'] = User.objects.get(id=result['createdBy']).username
        result['assigned'] = None
        if User.objects.filter(id=result['assignedTo']).exists():
            result['assigned'] = User.objects.get(id=result['assignedTo']).username
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_feeders(request):
    if not ROLE.isValidOperation(ROLE.KEY_FEEDER, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    allRecords = FeederModel.objects.all()
    finalResult = list()
    for record in allRecords:
        result = FeederSerializer(record).data
        result['station'] = None
        if StationModel.objects.filter(seq_num=result['stationId']).exists():
            result['station'] = StationModel.objects.get(seq_num=result['stationId']).name        
        result['username'] = User.objects.get(id=result['createdBy']).username
        result['assigned'] = None
        if User.objects.filter(id=result['assignedTo']).exists():
            result['assigned'] = User.objects.get(id=result['assignedTo']).username
        finalResult.append(result)
    return Response(finalResult, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_feeder(request):
    if not ROLE.isValidOperation(ROLE.KEY_FEEDER, ROLE.KEY_CREATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        assigned_to = payload['assignedTo']
        assignedTo = None
        if User.objects.filter(id=assigned_to).exists():
            assignedTo = User.objects.get(id=assigned_to)
        del payload['assignedTo'] 
        stationId = None
        if StationModel.objects.filter(seq_num=payload['stationId']).exists():
            stationId =StationModel.objects.get(seq_num=payload['stationId'])
        del payload['stationId']                 
        saved_data = FeederModel.objects.create(createdBy=user, assignedTo=assignedTo, stationId=stationId, **payload)
        result = FeederSerializer(FeederModel.objects.get(seq_num=saved_data.seq_num)).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def update_feeder(request):
    if not ROLE.isValidOperation(ROLE.KEY_FEEDER, ROLE.KEY_UPDATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = json.loads(request.body.decode())
        assigned_to = payload['assignedTo']
        assignedTo = None
        if User.objects.filter(id=assigned_to).exists():
            assignedTo = User.objects.get(id=assigned_to)
        del payload['assignedTo']
        stationId = None
        if StationModel.objects.filter(seq_num=payload['stationId']).exists():
            stationId =StationModel.objects.get(seq_num=payload['stationId'])
        del payload['stationId']                 
        FeederModel.objects.filter(seq_num=payload['seq_num']).update(assignedTo=assignedTo, **payload)
        result = FeederSerializer(FeederModel.objects.get(seq_num=payload['seq_num'])).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_feeder(request):
    if not ROLE.isValidOperation(ROLE.KEY_FEEDER, ROLE.KEY_DELETE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num = request.GET['seq_num']
        FeederModel.objects.filter(seq_num=seq_num).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)
