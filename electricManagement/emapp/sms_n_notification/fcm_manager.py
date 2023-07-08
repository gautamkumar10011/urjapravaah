import firebase_admin
from firebase_admin import credentials, messaging , auth
from accounts.models import User
from emapp.permission.models import UserFeeder
from emapp.station.models import StationModel

cred = credentials.Certificate("D:/BHEL/Urjapravaah/electricManagement/emapp/sms_n_notification/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def is_valid_firebase_auth_id_token(uuid, phone):
    try:
        user  = auth.get_user(uuid)
        if len(phone) >=10 and phone in user.phone_number:
            return True
    except Exception as e:
        return False
    return False


def send_firebase_notification(registration_token, dataObject):
    try:
        message = messaging.MulticastMessage(
            # notification=messaging.Notification(
            #     title=title,
            #     body=body
            # ),
            data=dataObject,
            tokens=registration_token,
        )
        response = messaging.send_multicast(message)
        print('Successfully sent message:', response)
    except Exception as e:
        Error_Message.objects.create(err_message="fcm_manager.send_firebase_notification : " + str(e))
        raise Exception(str(e))


def send_notification(feeder, payload, schedule):
    station = StationModel.objects.get(seq_num=feeder.stationId.seq_num)
    try:
        if User.objects.filter(username=feeder.contact).exists():
            user = User.objects.get(username=feeder.contact)
            tokens = user.notification_tokens
            if tokens != None and "firebase_token" in tokens:
                dataObject['seq_num'] = str(schedule.seq_num)
                dataObject['message'] = get_message(station, feeder, payload)
                send_firebase_notification(user.notification_tokens['firebase_token'], dataObject)
    except Exception as e:
        Error_Message.objects.create(err_message="fcm_manager.send_notification : "+ username + "  " + str(e))
        raise Exception(str(e))

def get_message(station, feeder, payload):
    message = "Hi Sir/Ma'am" 
    message += "\nYou have a schedule for power curtailment"
    message += "\nStation: " + station.name
    message += "\nFeeder: " + feeder.name
    message += "\nDate: " + payload['dateOn']
    message += "\nTime: " + payload['timeFrom'] + " - " + payload['timeTo']
    return message            