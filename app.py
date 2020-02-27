import os
from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
import logging
from dotenv import load_dotenv

from db import db
from Models.subscriber import SubscriberModel


load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

log = logging.getLogger('app.log')
log.setLevel(logging.DEBUG)

app_key = os.environ.get('GLOBE_APP_SECRET')
app_id = os.environ.get('GLOBE_APP_ID')
short_code = os.environ.get('GLOBE_SHORT_CODE')

levels = []
details = [{}]


@app.route('/globe/', methods=['GET'])
def get_globe_details():
    queries = request.args
    access_token = queries.get("access_token")
    subscriber_number = queries.get("subscriber_number")
    subscriber = SubscriberModel(subscriber_number, access_token)
    subscriber.save_to_db()
    subs = SubscriberModel.query.all()
    return jsonify(subs), 200


@app.before_first_request
def create_tables():
    db.create_all()


#testing
@app.route('/level/', methods=['GET'])
def get_level():
    queries = request.args
    level = queries.get("level")
    print(level)
    return jsonify("success"), 200


#testing
@app.route('/level/<int:level>', methods=['POST'])
def save_level(level):
    levels.append(level)
    return jsonify(levels), 200


@app.route('/inbound', methods=['POST'])
def accept_message():
    request_data = request.get_json()
    details.append({
        "dateTime": request_data['dateTime'],
        "destinationAddress": request_data['destinationAddress'],
        "message": request_data['message']
    })
    print(details)
    return jsonify({'message': 'Level has been sent'}), 200


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
