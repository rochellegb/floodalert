import os
import logging
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv

from db import db
from Models.subscriber import Subscribers
from Models.announcement import Announcements
from datetime import datetime


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


@app.route('/globe/', methods=['GET'])
def opt_in():
    access_token = request.args.get("access_token")
    subscriber_number = request.args.get("subscriber_number")
    new_subscriber = Subscribers(access_token=access_token,
                                 subscriber_number=subscriber_number)
    Subscribers.save_subscriber(new_subscriber)
    Announcements.message_after_opt_in(access_token, subscriber_number)
    subscribers = Subscribers.query.all()
    return render_template('subscribers.html', subscribers=subscribers, title='subscribers'), 200


@app.route('/globe/', methods=['POST'])
def stop_subscription():
    data = request.get_json()
    subscriber_number = data['unsubscribed']['subscriber_number']
    subscriber = Subscribers.query.filter_by(subscriber_number=subscriber_number).first()
    Subscribers.delete_subscriber(subscriber)
    subscribers = Subscribers.query.all()
    return render_template('subscribers.html', subscribers=subscribers, title='subscribers'), 200


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/inbound/', methods=['POST'])
def inbound():
    data = request.get_json()
    message = data['inboundSMSMessageList']['inboundSMSMessage'][0]['message']
    senderaddress = data['inboundSMSMessageList']['inboundSMSMessage'][0]['senderAddress']
    print(message, senderaddress[-10:])
    return jsonify(message)


@app.route('/sensor/', methods=['POST'])
def posts():
    req_data = request.get_json()

    height = req_data['ActualHeight']
    level = req_data['Level']
    message = req_data['Message']

    data = Announcements(height=height, level=level, message=message)
    Announcements.save_to_db(data)
    announcements = Announcements.query.all()

    return render_template('announcements.html', announcements=announcements, title='subscribers'), 200


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
