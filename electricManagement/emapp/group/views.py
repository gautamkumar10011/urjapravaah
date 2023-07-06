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
from emapp.role import ROLE
from emapp.group.models import GroupModel
from emapp.group.serializers import GroupSerializer


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_group(request):
    if not ROLE.isValidOperation(ROLE.KEY_GROUP, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num =  request.GET['seq_num']
        data = GroupModel.objects.get(seq_num=seq_num)
        result = GroupSerializer(data).data
        result['username'] = User.objects.get(id=result['createdBy']).username
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_groups(request):
    if not ROLE.isValidOperation(ROLE.KEY_GROUP, ROLE.KEY_READ, request.user.username):
        return Respnse(status=status.HTTP_401_UNAUTHORIZED)
    allRecords = GroupModel.objects.all()
    result = list()
    for record in allRecords:
        serialized_record = GroupSerializer(record).data
        serialized_record['username'] = User.objects.get(id = serialized_record['createdBy']).username       
        result.append(serialized_record)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_group(request):
    if not ROLE.isValidOperation(ROLE.KEY_GROUP, ROLE.KEY_CREATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        saved_data = GroupModel.objects.create(createdBy=user, **payload)
        result = GroupSerializer(GroupModel.objects.get(seq_num=saved_data.seq_num)).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def update_group(request):
    if not ROLE.isValidOperation(ROLE.KEY_GROUP, ROLE.KEY_UPDATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = json.loads(request.body.decode())
        GroupModel.objects.filter(seq_num=payload['seq_num']).update( **payload)
        result = GroupSerializer(GroupModel.objects.get(seq_num=payload['seq_num'])).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_group(request):
    if not ROLE.isValidOperation(ROLE.KEY_GROUP, ROLE.KEY_DELETE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num = request.GET['seq_num']
        GroupModel.objects.filter(seq_num=seq_num).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"errMessage":str(e)}, status=status.HTTP_400_BAD_REQUEST)