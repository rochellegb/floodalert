import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

app_key = os.environ.get('GLOBE_APP_SECRET')
app_id = os.environ.get('GLOBE_APP_ID')


@app.route('/store/')
def get_item(name):
    url = 'https://developer.globelabs.com.ph/oauth/access_token?app_id={}&app_secret={}&code={}'.format(app_id, app_key, )
    items = []
    queries = request.args
    items.append(name)
    print(queries.get("page"))
    print(queries.get("size"))
    return jsonify(items), 200


app.run(port=5000)
