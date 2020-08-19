import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

from db import db
from Models.subscribers import Subscribers
from Models.announcements import Announcements
import plot
import outbound


load_dotenv()
app = Flask(__name__)


log = logging.getLogger('app.log')
log.setLevel(logging.DEBUG)

app_key = os.environ.get('GLOBE_APP_SECRET')
app_id = os.environ.get('GLOBE_APP_ID')
short_code = os.environ.get('GLOBE_SHORT_CODE')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.before_first_request
def create_tables():
    db.create_all()


# registration to subscribe
@app.route('/globe/', methods=['GET'])
def opt_in():
    access_token = request.args.get("access_token")
    subscriber_number = request.args.get("subscriber_number")
    if Subscribers.find_by_number(subscriber_number):
        return {'message': "The subscriber with this number '{}' already exists.".format(subscriber_number)}, 400
    new_subscriber = Subscribers(access_token=access_token,
                                 subscriber_number=subscriber_number)
    Subscribers.save_subscriber(new_subscriber)
    subscribers = Subscribers.query.all()
    return render_template('subscribers.html', subscribers=subscribers, title='subscribers'), 200


# unsubscribe from receiving alerts
@app.route('/globe/', methods=['POST'])
def stop_subscription():
    data = request.get_json()
    subscriber_number = data['unsubscribed']['subscriber_number']
    subscriber = Subscribers.find_by_number(subscriber_number)
    subscribers = Subscribers.query.all()
    try:
        Subscribers.delete_subscriber(subscriber)
    except:
        return {"message": "There was an error deleting this subscriber"}, 400
    return render_template('subscribers.html', subscribers=subscribers, title='subscribers'), 200


# accepts message from globe subscriber
@app.route('/notify/', methods=['POST'])
def inbound():
    data = request.get_json()
    message = data['inboundSMSMessageList']['inboundSMSMessage'][0]['message']
    sender_address = data['inboundSMSMessageList']['inboundSMSMessage'][0]['senderAddress']
    print(message, sender_address[-10:])
    return jsonify(message)


# sending sensor data to db
@app.route('/', methods=['POST'])
def posts():
    req_data = request.args

    height = req_data['ActualHeight']
    level = req_data['Level']
    category_level = req_data['CategoryLevel']
    message = req_data['Message']

    datetime_obj = datetime.now()
    time_str = datetime_obj.strftime("%m/%d/%Y %H:%M")

    data = Announcements(height=height, level=level, category_level=category_level, time_posted=time_str)
    Announcements.save_to_db(data)
    announcements = Announcements.query.all()
    full_message = "As of {}. Ang sukat ng tubig sa Consolacion St. ay {} inches at itinataas na ang warning level sa {} or {}"
                    .format(time_str, height, message, category_level)

    if level > 0:
        subsribersID = Subscribers.query.all()
        for subscriber in subsribersID:
            outbound(Message=full_message, access_token=subscriber.access_token,
                     subscriber_number=subscriber.subscriber_number)

    return render_template('home.html', announcements=announcements, title='subscribers'), 200


@app.route('/', methods=['GET'])
def get():
    announcements = db.session.query(Announcements).all()
    return render_template('home.html', announcements=announcements, title='subscribers'), 200


@app.route('/day', methods=['GET'])
def get_day_plot():
    get_date = request.args.get("date")

    date = get_date.split('/')
    month = date[0]
    day = date[1]
    year = date[2]

    data = plot.plot_daily(month=month, day=day, year=year)

    return jsonify(data)


@app.route('/month', methods=['GET'])
def get_month_plot():
    get_date = request.args.get("date")

    date = get_date.split('/')
    month = date[0]
    year = date[2]

    data = plot.plot_monthly(month=month, year=year)
    return jsonify(data)


@app.route('/year', methods=['GET'])
def get_year_plot():
    get_date = request.args.get("date")

    date = get_date.split('/')
    year = date[2]

    data = plot.plot_yearly(year=year)
    return jsonify(data)


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)







