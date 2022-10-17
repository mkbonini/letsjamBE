# app/__init__.py: Flask application instance

from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config[‘SQLALCHEMY_DATABASE_URI’] = ‘sqlite:///’+ \
                os.path.join(basedir, ‘db.sqlite3’)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    display_email = db.Column(db.String(255))
    picture_url = db.Column(db.String(255))
    about = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, name, display_email, picture_url, about, zipcode):
        self.name = name
        self.display_email = display_email
        self.picture_url = picture_url
        self.about = about
        self.zipcode = zipcode

class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.string)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

user_instrument = db.Table('user_instrument',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('instrument_id', db.Integer, db.ForeignKey('instrument.id'), primary_key=True),
    db.Column('plays_or_needs', db.Integer)
)








class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel



from app import routes
