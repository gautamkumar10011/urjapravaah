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
from emapp.permission.models import GroupFeeder
from emapp.permission.serializers import GroupFeederSerializer
from emapp.feeder.models import FeederModel
from emapp.group.models import GroupModel
from emapp.role import ROLE


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_permissions(request):
    if not ROLE.isValidOperation(ROLE.KEY_PERMISSION, ROLE.KEY_CREATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)    
    try:
        username = request.user.username
        payloads = json.loads(request.body.decode())
        for payload in payloads:
            if not GroupModel.objects.filter(seq_num=payload['groupId']).exists():
                return Response({"message":"User does not exists"}, status=status.HTTP_400_BAD_REQUEST) 
            if not FeederModel.objects.filter(seq_num=payload['feederId']).exists():
                return Response({"message":"feeder does not exists"}, status=status.HTTP_400_BAD_REQUEST) 
            group = GroupModel.objects.get(seq_num=payload['groupId'])
            feeder = FeederModel.objects.get(seq_num=payload['feederId'])
            if not GroupFeeder.objects.filter(groupId=group,feederId=feeder).exists():
                GroupFeeder.objects.create(groupId=group, feederId=feeder)
        return Response(status=status.HTTP_200_OK) 
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_permissions(request):
    if not ROLE.isValidOperation(ROLE.KEY_PERMISSION, ROLE.KEY_DELETE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)      
    try:
        payloads = json.loads(request.body.decode())
        for payload in payloads:
            if 'id' in payload:
                GroupFeeder.objects.filter(id=payload['id']).delete()   
            elif "feederId" in payload and "groupId" in payload:
                feeder = FeederModel.objects.get(seq_num=payload['feederId'])
                group = GroupModel.objects.get(seq_num=payload['groupId'])
                GroupFeeder.objects.filter(groupId=group, feederId=feeder).delete()  ## need to chage
        return Response(status=status.HTTP_204_NO_CONTENT) 
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def group_feeder_mapping(request):   
    if not ROLE.isValidOperation(ROLE.KEY_PERMISSION, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)      
    try:
        user = User.objects.get(username=request.user.username)
        groupId = int(request.GET['groupId'])
        result = fetch_group_feeder(groupId)
        return Response(result,status=status.HTTP_200_OK) 
    except Exception as e:
        return Response({"errMessage": str(e), "result":None}, status=status.HTTP_400_BAD_REQUEST)         


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def fetch_group(request):
    allGroups = GroupModel.objects.all()
    result = list()
    for  group in allGroups:
        result.append({
            "groupId":group.seq_num,
            "groumName":group.name
        })
    return Response(result,status=status.HTTP_200_OK)    

@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def group_feeder_mapping_only(request):   
    if not ROLE.isValidOperation(ROLE.KEY_PERMISSION, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)      
    try:
        user = User.objects.get(username=request.user.username)
        groupId = int(request.GET['groupId'])
        result = fetch_only_group_feeder_mapped(groupId)
        return Response(result,status=status.HTTP_200_OK) 
    except Exception as e:
        return Response({"errMessage": str(e), "result":None}, status=status.HTTP_400_BAD_REQUEST)

def fetch_group_feeder(groupId):
    group = GroupModel.objects.get(seq_num=groupId)
    groupFeeders = GroupFeeder.objects.filter(groupId=group)
    allFeeders = FeederModel.objects.all()
    result = list()
    feederMap = dict()
    for groupFeeder in groupFeeders:
        if groupFeeder.feederId.seq_num not in feederMap:
            result.append({
                "groupId" : groupId,
                "groupName": group.name,
                "feederId": groupFeeder.feederId.seq_num,
                "feederName": groupFeeder.feederId.name,
                "hasMapping":True
            }
            )
            feederMap[groupFeeder.feederId.seq_num] = True
    for feeder in allFeeders:
        if feeder.seq_num not in feederMap:
            result.append({
                "groupId" : groupId,
                "groupName": group.name,
                "feederId": feeder.seq_num,
                "feederName": feeder.name,
                "hasMapping":False
            }
            )
            feederMap[feeder.seq_num] = True
    return result


def fetch_only_group_feeder_mapped(groupId):
    group = GroupModel.objects.get(seq_num=groupId)
    groupFeeders = GroupFeeder.objects.filter(groupId=group)
    result = list()
    feederMap = dict()
    for groupFeeder in groupFeeders:
        if groupFeeder.feederId.seq_num not in feederMap:
            result.append({
                "groupId" : groupId,
                "groupName": group.name,
                "feederId": groupFeeder.feederId.seq_num,
                "feederName": groupFeeder.feederId.name,
                "hasMapping":True
            }
            )
            feederMap[groupFeeder.feederId.seq_num] = True

    return result