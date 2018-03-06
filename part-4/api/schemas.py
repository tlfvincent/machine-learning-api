import datetime
from api import db


class Classifications(db.Model):

    __tablename__ = 'classifications'

    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.String, nullable=True)
    response = db.Column(db.String, nullable=True)
    status_code = db.Column(db.Integer, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=True)

    def __init__(self, text, payload, status_code):
        self.text = text
        self.payload = payload
        self.status_code =  status_code
        self.date_posted = datetime.datetime.now()

