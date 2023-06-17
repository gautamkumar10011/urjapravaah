import json
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count , Sum , F , Value
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
) 
from django.conf import settings
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import User
from .serializers import UserSerializer
from emapp.role import ROLE
from emapp.role.models import UserRoleModel
PAGE_SIZE = 25


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_user_by_id(request):
    # if not ROLE.isValidOperation(ROLE.KEY_USER, ROLE.KEY_READ, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)    
    try:
        user_id =  request.GET['id']
        user = UserSerializer(User.objects.get(id=user_id)).data
        user["role_name"] = ""
        if UserRoleModel.objects.filter(seq_num=user["roleId"]).exists():
            user["role_name"] = UserRoleModel.objects.get(seq_num=user["roleId"]).name        
        return Response(user, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)},status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_all_users(request):
    # if not ROLE.isValidOperation(ROLE.KEY_USER, ROLE.KEY_READ, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
    if 'search_key' in request.GET:
        users = User.objects.filter(Q(username__icontains=request.GET['search_key'])|Q(first_name__icontains=request.GET['search_key']))
    else:
        users = User.objects.all()
    
    paginator = PageNumberPagination()
    paginator.page_size = PAGE_SIZE
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)
    for user in serializer.data:
        user["role_name"] = ""
        if UserRoleModel.objects.filter(seq_num=user["roleId"]).exists():
            user["role_name"] = UserRoleModel.objects.get(seq_num=user["roleId"]).name
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def get_all_users_mapping(request):
    # if not ROLE.isValidOperation(ROLE.KEY_USER, ROLE.KEY_READ, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
    if "search_key" in request.GET:
        users = User.objects.filter(Q(first_name__icontains=request.GET['search_key'],is_public=False))
    else:
        users = User.objects.filter(is_public=False)
    serializer = UserSerializer(users, many=True).data
    for user in serializer:
        user["role_name"] = ""        
        if UserRoleModel.objects.filter(seq_num=user["roleId"]).exists():
            user["role_name"] = UserRoleModel.objects.get(seq_num=user["roleId"]).name        
    return Response(serializer, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def create_user(request):
    # if not ROLE.isValidOperation(ROLE.KEY_USER, ROLE.KEY_CREATE, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)     
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        if User.objects.filter(username=payload['username']).exists():
            return Response({"error":"Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
        if len(payload['password']) <= 8:
            return Response({"error":"password length too short, should be grater than 8"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone=payload['phone']).exists():
            return Response({"error":"phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        password = payload['password']
        if 'id' in payload: del payload['id']
        roleId = get_reference_model_object(payload, user)
        clean_user_payload_data(payload)
        user = User(roleId=roleId, **payload)
        user.set_password(password)
        user.save()
        result = UserSerializer(User.objects.get(username=payload['username'])).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage":str(e)},status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def update_user(request):
    # if not ROLE.isValidOperation(ROLE.KEY_USER, ROLE.KEY_UPDATE, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)     
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        villageId, blockId, districtId, roleId = get_reference_model_object(payload, user)
        clean_user_payload_data(payload)
        if 'username' in payload : del payload['username']
        User.objects.filter(id=payload['id']).update(roleId=roleId, **payload)
        result = UserSerializer(User.objects.get(id= payload['id'])).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def delete_user(request):
    # if not ROLE.isValidOperation(ROLE.KEY_USER, ROLE.KEY_DELETE, request.user.username):
        # return Response(status=status.HTTP_401_UNAUTHORIZED)     
    try:
        id = request.GET['id']
        User.objects.filter(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def clean_user_payload_data(payload):
    if "roleId" in payload:
        del payload['roleId']
    if "is_superuser" in payload:
        del payload['is_superuser']
    if 'password' in payload:
        del payload['password']



def get_reference_model_object(payload, user):
    roleId = user.roleId

    if "roleId" in payload:
        if payload['roleId'] != None:
            roleId = UserRoleModel.objects.get(seq_num=payload['roleId'])
        else:
            roleId = None
    return roleId