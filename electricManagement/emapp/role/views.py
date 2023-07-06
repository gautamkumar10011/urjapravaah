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
from emapp.role.models import UserRoleModel
from emapp.role.serializers import UserRoleSerializer
from .models import CRUDModel
from .serializers import CRUDSerializer
from emapp.role import ROLE
from emapp.role.models import ComponetName
from emapp.role.serializers import ComponetNameSerializer
from datetime import datetime
CRUD_BINARY = ["0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111"]



@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_role(request):
    if not ROLE.isValidOperation(ROLE.KEY_ROLE, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)           
    try:
        role_id =  request.GET['seq_num']
        result = UserRoleSerializer(UserRoleModel.objects.get(seq_num=role_id)).data
        return Response(result, status=status.HTTP_200_OK)    
    except Exception as e:
        return Response({"errMessage": str(e) },status=status.HTTP_404_NOT_FOUND)             


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_roles(request):
    if not ROLE.isValidOperation(ROLE.KEY_ROLE, ROLE.KEY_READ, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED) 
    result = UserRoleSerializer(UserRoleModel.objects.all(), many=True).data
    return Response(result, status=status.HTTP_200_OK)  


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_role(request):
    if not ROLE.isValidOperation(ROLE.KEY_ROLE, ROLE.KEY_CREATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)               
    try:
        username = request.user.username
        createdBy = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        if 'seq_num' in payload: del payload['seq_num']
        saved_data = UserRoleModel.objects.create(name=payload['name'], 
        createdBy=createdBy,
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
        feeder=CRUDModel.objects.get(value=payload['feeder']),
        station=CRUDModel.objects.get(value=payload['station']),
        schedule=CRUDModel.objects.get(value=payload['schedule']),
        role=CRUDModel.objects.get(value=payload['role']),
        urjauser=CRUDModel.objects.get(value=payload['urjauser']),
        control_panel=CRUDModel.objects.get(value=payload['control_panel']),
        group=CRUDModel.objects.get(value=payload['group']))
        result = UserRoleSerializer(UserRoleModel.objects.get(seq_num=saved_data.seq_num)).data
        return Response(result, status=status.HTTP_200_OK)  
    except Exception as e:
        return Response({"Exception": str(e)},status=status.HTTP_400_BAD_REQUEST)    


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def update_role(request):
    if not ROLE.isValidOperation(ROLE.KEY_ROLE, ROLE.KEY_UPDATE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)               
    try:
        username = request.user.username
        createdBy = User.objects.get(username=username)        
        payload = json.loads(request.body.decode())
        del payload['createdBy']
        UserRoleModel.objects.filter(seq_num=payload['seq_num']).update(name=payload['name'], 
        createdBy=createdBy,
        createdAt=payload['createdAt'],
        updatedAt=datetime.now(),
        feeder=CRUDModel.objects.get(value=payload['feeder']),
        station=CRUDModel.objects.get(value=payload['station']),
        schedule=CRUDModel.objects.get(value=payload['schedule']),
        role=CRUDModel.objects.get(value=payload['role']),
        urjauser=CRUDModel.objects.get(value=payload['urjauser']),
        control_panel=CRUDModel.objects.get(value=payload['control_panel']),
        group=CRUDModel.objects.get(value=payload['group']))        
        result = UserRoleSerializer(UserRoleModel.objects.get(seq_num=payload['seq_num'])).data
        return Response(result, status=status.HTTP_200_OK) 
    except Exception as e:
        return Response({"Exception": str(e)}, status=status.HTTP_400_BAD_REQUEST)     


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_role(request):
    if not ROLE.isValidOperation(ROLE.KEY_ROLE, ROLE.KEY_DELETE, request.user.username):
        return Response(status=status.HTTP_401_UNAUTHORIZED)               
    try:
        role_id = request.GET['seq_num']
        UserRoleModel.objects.filter(seq_num=role_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    except Exception as e:
        Error_Message.objects.create(err_message="delete_role : " + str(e))
        return Response(status=status.HTTP_400_BAD_REQUEST)        
    

@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def crud_name_n_value(request):
    result = CRUDSerializer(CRUDModel.objects.all(), many=True).data
    for record in result:
        record['binary'] = CRUD_BINARY[record['value']]    
    return Response(result, status=status.HTTP_200_OK) 


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def compnent_name(request):
    compnent = ComponetName.objects.order_by("displayName")
    result = ComponetNameSerializer(compnent, many=True).data
    i = 1 
    for data in result:
        data['id'] = i
        i += 1
    return Response(result, status=status.HTTP_200_OK) 


def isUserAdmin(roleId):
    role = UserRoleModel.objects.get(seq_num=roleId)
    result = UserRoleSerializer(role).data
    if result['control_panel'] == 15 and \
       result['feeder'] == 15 and \
       result['station'] == 15 and \
       result['schedule'] == 15 and \
       result['role'] == 15 and \
       result['urjauser'] == 15: 
        return True
    else:
        return False
