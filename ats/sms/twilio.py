import os
from twilio.rest import Client

account_sid = os.environ.get('TWILIO_ACCOUNT_SID', None)
auth_token = os.environ.get('TWILIO_AUTH_TOKEN', None)

number_from = os.environ.get('TWILIO_PHONE_NUMBER', None)
number_to = os.environ.get('NOTIFY_PHONE_NUMBER', None)

# TOOD: make this a class.
client = None

def send_notification(msg):
    global client
    if not client:
        client = Client(account_sid, auth_token)

    message = client.messages \
                .create(
                     body=msg,
                     from_=number_from,
                     to=number_to
                 )
    print("SMS SID:", message.sid)
