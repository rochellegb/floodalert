import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

app_key = os.environ.get('GLOBE_APP_SECRET')
app_id = os.environ.get('GLOBE_APP_ID')

subscriber_numbers = []
access_tokens = []


@app.route('/globe/')
def get_globe_details():
    queries = request.args
    access_token = queries.get("access_token")
    subscriber_number = queries.get("subscriber_number")
    access_tokens.append(access_token)
    subscriber_numbers.append(subscriber_number)
    return jsonify(access_tokens, subscriber_numbers), 200


@app.route('/access_token/', methods=['POST'])
def post_globe_details():
    url = 'https://developer.globelabs.com.ph/oauth/access_token?app_id={}&app_secret={}&code={}'.format(app_id, app_key, '')
    queries = request.args
    print(queries.get("app_id"))
    print(queries.get("app_secret"))
    return jsonify(), 200


app.run(port=5000)
