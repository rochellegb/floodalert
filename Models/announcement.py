import os
from dotenv import load_dotenv
from db import db
from datetime import datetime
import requests

load_dotenv()

short_code = os.environ.get('GLOBE_SHORT_CODE')


class Announcements(db.Model):
    __tablename__ = "Announcements"

    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float())
    level = db.Column(db.Integer)
    message = db.Column(db.String(250))
    posted = db.Column(db.DateTime, default=datetime.now)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #outbound every level
    def message_to_many(self, access_token, sender_address, message):
        shortcode = short_code[-4:]
        access_token = access_token
        address = sender_address
        clientCorrelator = '268401'
        message = message

        url = "https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/" + shortcode + "/requests"

        querystring = {"access_token": access_token}

        payload = "{\"outboundSMSMessageRequest\": { \"clientCorrelator\": \"" + clientCorrelator + "\", \"senderAddress\": \"" + shortcode + "\", \"outboundSMSTextMessage\": {\"message\": \"" + message + "\"}, \"address\": \"" + address + "\" } }"
        headers = {'Content-Type': "application/json", 'Host': "devapi.globelabs.com.ph"}

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        print(response.text)

    #outbound for update
    def message_after_opt_in(access_token, subscriber_number):
        shortcode = short_code[-4:]
        access_token = access_token
        address = subscriber_number
        clientCorrelator = '268401'
        message = "Hello"

        url = "https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/" + shortcode + "/requests"

        querystring = {"access_token": access_token}

        payload = "{\"outboundSMSMessageRequest\": { \"clientCorrelator\": \"" + clientCorrelator + "\", \"senderAddress\": \"" + shortcode + "\", \"outboundSMSTextMessage\": {\"message\": \"" + message + "\"}, \"address\": \"" + address + "\" } }"
        headers = {'Content-Type': "application/json", 'Host': "devapi.globelabs.com.ph"}

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        print(response.text)