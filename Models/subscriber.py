import os
from db import db
from dotenv import load_dotenv
import requests

load_dotenv()

short_code = os.environ.get('GLOBE_SHORT_CODE')


class Subscribers(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(100))
    subscriber_number = db.Column(db.Integer)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    def delete_subscriber(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_number(cls, subscriber_number):
        return cls.query.filter_by(subscriber_number=subscriber_number).first()

    #outbound every level
    def message_to_many(self, message):
        shortcode = short_code[-4:]
        access_token = self.access_token
        address = self.subscriber_number
        clientCorrelator = '268401'
        message = message

        url = "https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/" + shortcode + "/requests"

        querystring = {"access_token": access_token}

        payload = "{\"outboundSMSMessageRequest\": { \"clientCorrelator\": \"" + clientCorrelator + "\", \"senderAddress\": \"" + shortcode + "\", \"outboundSMSTextMessage\": {\"message\": \"" + message + "\"}, \"address\": \"" + address + "\" } }"
        headers = {'Content-Type': "application/json", 'Host': "devapi.globelabs.com.ph"}

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        print(response.text)
