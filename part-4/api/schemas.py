import datetime
from api import db


class Classifications(db.Model):

    __tablename__ = 'classifications'

    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.String, nullable=True)
    response = db.Column(db.String, nullable=True)
    status_code = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, payload, response, status_code, datestamp):
        self.payload = payload
        self.response = response
        self.status_code = status_code
        self.created_at = datestamp
