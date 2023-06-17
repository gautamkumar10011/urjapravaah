import firebase_admin
from firebase_admin import credentials, messaging , auth
from accounts.models import User

cred = credentials.Certificate("D:\BHEL\electricManagement\emapp\sms_n_notification\serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def is_valid_firebase_auth_id_token(uuid, phone):
    try:
        user  = auth.get_user(uuid)
        if len(phone) >=10 and phone in user.phone_number:
            return True
    except Exception as e:
        return False
    return False
