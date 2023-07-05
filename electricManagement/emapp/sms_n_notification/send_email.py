from django.core.mail import send_mail
from django.conf import settings
from emapp.station.models import StationModel


def send_email_to_station(feeder, payload):
    station = StationModel.objects.get(seq_num=feeder.stationId.seq_num)
    subject = "Urja Pravaah, Schedule Notification"
    message = "You have scheduled for power distribution date on " + payload['dateOn'] + \
    " from " + payload['timeFrom'] + " to " + payload['timeTo'] + "."
    from_email = settings.EMAIL_HOST_USER
    recepient_list = [station.email]
    send_mail(subject,message,from_email,recepient_list,auth_password=settings.EMAIL_HOST_PASSWORD)