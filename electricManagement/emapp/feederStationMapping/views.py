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
from emapp.feederStationMapping.models import FeederStationModel
from emapp.feederStationMapping.serializers import FeederStationSerializer
from emapp.role import ROLE


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_feederStation(request):
    # if not ROLE.isValidOperation(ROLE.KEY_STATE, ROLE.KEY_READ, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num =  request.GET['seq_num']
        result = FeederStationSerializer(FeederStationModel.objects.get(seq_num=seq_num)).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage" : str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_feederStations(request):
    # if not ROLE.isValidOperation(ROLE.KEY_STATE, ROLE.KEY_READ, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
    result = FeederStationSerializer(FeederStationModel.objects.all(),many=True).data
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_feederStation(request):
    # if not ROLE.isValidOperation(ROLE.KEY_STATE, ROLE.KEY_CREATE, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        saved_data = FeederStationModel.objects.create(createdBy=user, **payload)
        result = FeederStationSerializer(FeederStationModel.objects.get(seq_num=saved_data.seq_num)).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage" : str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def update_feederStation(request):
    # if not ROLE.isValidOperation(ROLE.KEY_STATE, ROLE.KEY_UPDATE, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = json.loads(request.body.decode())
        created_by = payload['createdBy']
        createdBy = User.objects.get(id=created_by)
        del payload['createdBy']
        FeederStationModel.objects.filter(seq_num=payload['seq_num']).update(createdBy=createdBy, **payload)
        result = FeederStationSerializer(FeederStationModel.objects.get(seq_num=payload['seq_num'])).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage" : str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_feederStation(request):
    # if not ROLE.isValidOperation(ROLE.KEY_STATE, ROLE.KEY_DELETE, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        seq_num = request.GET['seq_num']
        FeederStationModel.objects.filter(seq_num=seq_num).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"errMessage" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
