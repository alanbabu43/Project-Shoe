from django.conf import settings
from twilio.rest import Client
import random

class MassHandler:


    phone_number = None
    otp =None

    def _init_(self,phone_number , otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_on_phone(self):  
        client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)


        message = client.messages.create(
                              body=f'your otp is: {self.otp}',
                              from_=f'{settings.TWILIO_PHONE_NUMBER}',
                              to=f'{settings.COUNTRY_CODE}{self.phone_number}'
                              )
        print(message.sid)