import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

number_from = os.environ['TWILIO_PHONE_NUMBER']
number_to = os.environ['NOTIFY_PHONE_NUMBER']

client = Client(account_sid, auth_token)

def send_notification(msg):
    message = client.messages \
                .create(
                     body=msg,
                     from_=number_from,
                     to=number_to
                 )
    print("SMS SID:", message.sid)
