import requests


def outbound(message, access_token, subscriber_number):

    short_code = '7128'
    access_token = access_token
    address = subscriber_number
    clientCorrelator = '21587128'
    message = message

    url = "https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/"+short_code+"/requests"

    querystring = {"access_token": access_token}

    payload = "{\"outboundSMSMessageRequest\": { \"clientCorrelator\": \""+clientCorrelator+"\", 
                \"senderAddress\": \""+short_code+"\", 
                \"outboundSMSTextMessage\": {\"message\": \""+message+"\"}, 
                \"address\": \""+address+"\" } }"
    headers = {'Content-Type': "application/json", 'Host': "devapi.globelabs.com.ph"}

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    return response.text
