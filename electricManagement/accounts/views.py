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
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
) 
from django.conf import settings
from .models import User
from accounts.serializers import UserSerializer
from emapp.role.models import UserRoleModel
from emapp.role.serializers import UserRoleSerializer
from emapp.sms_n_notification.fcm_manager import is_valid_firebase_auth_id_token
from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_me(request):
    try:
        login_data = json.loads(request.body.decode())
        if 'phone' in login_data and 'uuid' in login_data:  
            phone, uuid = login_data['phone'], login_data['uuid']
            return login_user(phone, uuid)
        return Response(status=HTTP_400_BAD_REQUEST )
    except Exception as e: 
        return Response({"errMessage": str(e)}, status=HTTP_400_BAD_REQUEST )  


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def update_notification_token(request):
    try:
        username = request.user.username
        payload = json.loads(request.body.decode())
        user = User.objects.get(username=username)
        notification_tokens = user.notification_tokens
        if notification_tokens != None and "firebase_token" in notification_tokens:
            if payload['firebase_token'] != None and payload['firebase_token'] not in notification_tokens['firebase_token']:
                notification_tokens['firebase_token'].append(payload['firebase_token'])
        else:
            if notification_tokens == None:
                notification_tokens = dict()
                notification_tokens['firebase_token'] = list()
            if payload['firebase_token'] != None:
                notification_tokens['firebase_token'].append(payload['firebase_token'])
        User.objects.filter(username=username).update(notification_tokens=notification_tokens)
        result = UserSerializer(User.objects.get(username=username)).data
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errMessage": str(e)}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode())
        notification_tokens = user.notification_tokens
        if notification_tokens != None and "firebase_token" in notification_tokens:
            if payload['firebase_token'] != None and payload['firebase_token'] in notification_tokens['firebase_token']:
                notification_tokens['firebase_token'].remove(payload['firebase_token'])
        User.objects.filter(username=username).update(notification_tokens=notification_tokens)
        return Response(status=HTTP_204_NO_CONTENT)   
    except Exception as e:
        return Response({"errMessage": str(e)}, status=status.HTTP_404_NOT_FOUND)          


def user_profile(username):
    user = User.objects.get(username=username)
    token, _ = Token.objects.get_or_create(user=user)
    user.last_login = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    user.save()
    result = UserSerializer(user).data
    userrole = None
    if UserRoleModel.objects.filter(seq_num=result['roleId']).exists() :
        userrole = UserRoleSerializer(UserRoleModel.objects.get(seq_num=result['roleId'])).data
    return Response({ "user": result, "token": token.key , "userrole" : userrole}, status=HTTP_200_OK)


def login_user(phone, uuid):
    if is_valid_firebase_auth_id_token(uuid,phone):
        print("passed the test")
        return user_profile(phone)
    return Response({"status": 401},status=HTTP_401_UNAUTHORIZED)
