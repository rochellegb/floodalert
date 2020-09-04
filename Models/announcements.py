from db import db


class Announcements(db.Model):
    __tablename__ = "Announcements"

    id = db.Column(db.Integer, primary_key=True)
    time_posted = db.Column(db.String(250))
    height = db.Column(db.Float())
    level = db.Column(db.Integer)
    category_level = db.Column(db.String(250))
    # message = db.Column(db.String(250))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return f'{self.id}: {self.height}, {self.level}, {self.time_posted}'

    def __repr__(self):
        return f'Announcements({self.id}: {self.height}, {self.level}, {self.time_posted})'



