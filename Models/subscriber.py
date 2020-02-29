from db import db


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

