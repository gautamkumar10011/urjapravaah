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

    user_feeders = UserFeeder.objects.filter(userId=user).values_list('feederId__stationId', flat=True)
    unique_stations = set(user_feeders)
    stations = StationModel.objects.filter(seq_num__in=unique_stations)
    result = StationSerializer(stations, many=True).data
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



@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def upload_file(request):
    try:
        createdBy = User.objects.get(username=request.user.username)
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return Response({"errMessage":"File should be csv."}, status=status.HTTP_400_BAD_REQUEST)
        if csv_file.multiple_chunks():
            message = "Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000))
            return Response({"errMessage": message}, status=status.HTTP_400_BAD_REQUEST)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        first_line = 0
        for line in lines:
            try:
                if first_line != 0:
                    print(line)
                    fields = line.split(",")
                    print(len(fields))
                    ## Station ##
                    if not StationModel.objects.filter(name=fields[6]).exists():
                        name = fields[6]
                        stationManager = fields[12]
                        stationCode = fields[6]
                        contact = fields[15]
                        latitude = float(fields[9].replace("\"",''))
                        longitude = float(fields[10].replace("\"",''))
                        email = fields[14]
                        capacity = fields[7]
                        StationModel.objects.create(name=name, stationManager=stationManager, stationCode=stationCode,
                            contact=contact, latitude=latitude, longitude=longitude, email=email, createdBy=createdBy, capacity=capacity)

                    ### Feeder ###
                    stationId = StationModel.objects.get(name=fields[6])
                    name = fields[16]
                    feederManager = fields[12]
                    feederCode = fields[16]
                    contact = fields[15]
                    latitude = float(fields[9].replace("\"",''))
                    longitude = float(fields[10].replace("\"",''))
                    feederType = fields[17]
                    FeederModel.objects.create(name=name,feederManager=feederManager, feederCode=feederCode, contact=contact,
                    stationId=stationId, latitude=latitude, longitude=longitude, createdBy=createdBy, feederType=feederType)
            except Exception as e:
                return Response({"errMessage":str(e)},status=status.HTTP_400_BAD_REQUEST)
            first_line += 1
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"errMessage":str(e)},status=status.HTTP_400_BAD_REQUEST)
