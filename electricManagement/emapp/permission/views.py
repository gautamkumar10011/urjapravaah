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
from emapp.permission.models import UserFeeder
from emapp.permission.serializers import UserFeederSerializer
from emapp.feeder.models import FeederModel
from emapp.role import ROLE
from emapp.role.views import isUserAdmin


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_permissions(request):
    # if not ROLE.isValidOperation(ROLE.KEY_PERMISSION, ROLE.KEY_CREATE, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)    
    try:
        username = request.user.username
        payloads = json.loads(request.body.decode())
        for payload in payloads:
            if not User.objects.filter(id=payload['userId']).exists():
                return Response({"message":"User does not exists"}, status=status.HTTP_400_BAD_REQUEST) 
            if not FeederModel.objects.filter(seq_num=payload['feederId']).exists():
                return Response({"message":"feeder does not exists"}, status=status.HTTP_400_BAD_REQUEST) 
            user = User.objects.get(id=payload['userId'])
            feeder = FeederModel.objects.get(seq_num=payload['feederId'])
            if not UserFeeder.objects.filter(userId=user,feederId=feeder).exists():
                UserFeeder.objects.create(userId=user, feederId=feeder)
        return Response(status=status.HTTP_200_OK) 
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_permissions(request):
    # if not ROLE.isValidOperation(ROLE.KEY_PERMISSION, ROLE.KEY_DELETE, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)      
    try:
        payloads = json.loads(request.body.decode())
        for payload in payloads:
            if 'id' in payload:
                UserFeeder.objects.filter(id=payload['id']).delete()   
            elif "feederId" in payload and "userId" in payload:
                feeder = FeederModel.objects.get(id=payload['feederId'])
                user = User.objects.get(id=payload['userId'])
                UserFeeder.objects.filter(userId=user, feederId=feeder).delete()  ## need to chage
        return Response(status=status.HTTP_204_NO_CONTENT) 
    except Exception as e:
        return Response({"status": 400, "result":None}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def feeder_mapping(request):   
    # if not ROLE.isValidOperation(ROLE.KEY_PERMISSION, ROLE.KEY_READ, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)      
    try:
        user = User.objects.get(username=request.user.username)
        userId = int(request.GET['userId'])
        if isUserAdmin(user.roleId.seq_num):
            result = get_device_user_mapping(userId)
        else:
            result = fetch_user_devices(userId, user)
        return Response(result,status=status.HTTP_200_OK) 
    except Exception as e:
        return Response({"errMessage": str(e), "result":None}, status=status.HTTP_400_BAD_REQUEST)         


def get_device_user_mapping(userId):
    user = User.objects.get(id=userId)
    userFeeders = UserFeeder.objects.filter(user=user)
    allFeeders = FeederModel.objects.all()
    result = list()
    feederMap = dict()
    for userFeeder in userFeeders:
        if userFeeder.feederId.seq_num not in deviceMap:
            result.append({
                "user" : userId,
                "username": user.username,
                "feederId": userFeeder.feederId.seq_num,
                "feederName": userFeeder.feeder.name,
                "hasMapping":True
            }
            )
            deviceMap[userDevice.device.id] = True

    for feeder in allFeeders:
        if feeder.seq_num not in feederMap:
            result.append({
                "user" : userId,
                "username": user.username,
                "feederId": device.seq_num,
                "feederName": device.name,
                "hasMapping":False
            }
            )
            feederMap[feeder.seq_num] = True
    return result


def fetch_user_devices(userId, user1):
    user = User.objects.get(id=userId)
    userFeeders = UserFeeder.objects.filter(userId=user)
    allFeeders = UserFeeder.objects.filter(user=user1)
    result = list()
    feederMap = dict()
    for userFeeder in userFeeders:
        if userDevice.device.id not in deviceMap:
            result.append({
                "user" : userId,
                "username": user.username,
                "feederId": userFeeder.feederId.seq_num,
                "feederName": userFeeder.feederId.name,
                "hasMapping":True
            }
            )
            feederMap[userFeeder.feederId.seq_num] = True

    for feeder in allFeeders:
        if feeder.feederId.seq_num not in deviceMap:
            result.append({
                "user" : userId,
                "username": user.username,
                "feederId": feeder.feederId.seq_num,
                "device_id": feeder.feederId.name,
                "hasMapping":False
            }
            )
            feederMap[feeder.feederId.seq_num] = True
    return result