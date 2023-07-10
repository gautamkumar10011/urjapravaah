import django
django.setup()
from django.core.mail import send_mail
from django.conf import settings
from emapp.station.models import StationModel


def send_email_to_station(feeder, payload):
    station = StationModel.objects.get(seq_num=feeder.stationId.seq_num)
    subject = "Urja Pravaah, Schedule Notification"
    message = "Hi Sir/Ma'am" 
    message += "\nYou have a schedule for power curtailment"
    message += "\nStation: " + station.name
    message += "\nFeeder: " + feeder.name
    message += "\nDate: " + payload['dateOn']
    message += "\nTime: " + payload['timeFrom'] + " - " + payload['timeTo']
    message += "\nPoc Name: " + feeder.feederManager
    message += "\nPoc Contact: " + feeder.contact
    message += "\n\nRegards\nJPDCL"
    from_email = settings.EMAIL_HOST_USER
    recepient_list = [station.email]
    send_mail(subject,message,from_email,recepient_list,auth_password=settings.EMAIL_HOST_PASSWORD)