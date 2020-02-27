from db import db
import sqlite3


class SubscriberModel(db.Model):
    __tablename__ = "subscribers"

    id = db.Column(db.Integer, primary_key=True)
    subscriber_number = db.Column(db.Integer)
    access_token = db.Column(db.Integer)

    def __init__(self, subscriber_number, access_token):
        self.subscriber_number = subscriber_number
        self.access_token = access_token

    def json(self):
        return {'subscriber_number': self.subscriber_number, 'access_token': self.access_token}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
