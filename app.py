import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

app_key = os.environ.get('GLOBE_APP_SECRET')
app_id = os.environ.get('GLOBE_APP_ID')


#missing redirect uri
@app.route('/code/', methods=['GET'])
def get_globe_code():
    queries = request.args
    code = queries.get("code")
    print(code)
    return jsonify("success"), 200


@app.route('/access_token/', methods=['POST'])
def post_globe_details():
    url = 'https://developer.globelabs.com.ph/oauth/access_token?app_id={}&app_secret={}&code={}'.format(app_id, app_key, '')
    queries = request.args
    print(queries.get("app_id"))
    print(queries.get("app_secret"))
    return jsonify(), 200


app.run(port=5000)
