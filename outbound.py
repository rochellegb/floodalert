import os
from dotenv import load_dotenv
import requests

load_dotenv()

short_code = os.environ.get('GLOBE_SHORT_CODE')


shortcode = short_code[-4:]
access_token = '1UAMW2nbi6l6gCw8wG_djbt_NiT7JSqwmyqhtsXUK2g'
address = '9773005800'
clientCorrelator = '268401'
message = 'WAZZUP THIS IS GLOBE'

url = "https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/" + shortcode + "/requests"

querystring = {"access_token": access_token}

payload = "{\"outboundSMSMessageRequest\": { \"clientCorrelator\": \"" + clientCorrelator + "\", \"senderAddress\": \"" + shortcode + "\", \"outboundSMSTextMessage\": {\"message\": \"" + message + "\"}, \"address\": \"" + address + "\" } }"
headers = {'Content-Type': "application/json", 'Host': "devapi.globelabs.com.ph"}

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)