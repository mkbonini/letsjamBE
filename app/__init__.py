# app/__init__.py: Flask application instance

from flask import Flask
import os
import enum
from flask import request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Integer, ForeignKey, String, Column, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://nrjdztyzcfvwlk:d767f32cd3f5645fb1dbf2322b6b5f93a3ba723cc625bcdc67f7cce3db369d16@ec2-44-199-9-102.compute-1.amazonaws.com:5432/d5i6c3pfolni3l"

db = SQLAlchemy(app)
ma = Marshmallow(app)

Base = declarative_base()

class ConnectionStatus(enum.Enum):
    APPROVED = "Approved"
    PENDING = "Pending"
    REJECTED = "Rejected"

user_instrument = db.Table('user_instrument', Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('instrument_id', db.Integer, db.ForeignKey('instrument.id'), primary_key=True),
    db.Column('plays_or_needs', db.Integer)
)

user_genre = db.Table('user_genre', Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

user_connection = db.Table('user_connection', Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    # db.Column(db.Enum(ConnectionStatus))
)

class User(Base):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    display_email = db.Column(db.String(255))
    picture_url = db.Column(db.String(255))
    about = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    instruments = db.relationship('Instrument', secondary=user_instrument, lazy='dynamic', backref=db.backref('users', lazy=True))
    genres = db.relationship('Genre', secondary=user_genre, lazy='dynamic', backref=db.backref('users', lazy=True))
    connections = db.relationship('User', secondary=user_connection, primaryjoin=id == user_connection.c.user_id, secondaryjoin=id == user_connection.c.friend_id, lazy='dynamic', backref=db.backref('users', lazy=True))

    def __init__(self, name, display_email, picture_url, about, zipcode):
        self.name = name
        self.display_email = display_email
        self.picture_url = picture_url
        self.about = about
        self.zipcode = zipcode

class Instrument(Base):
    __tablename__ = "instrument"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name


class Genre(Base):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class InstrumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Instrument

instrument_schema = InstrumentSchema()
instruments_schema = InstrumentSchema(many=True)




@app.route('/users/<int:user_id>/')
def show_user(user_id):
    user = User.query.get(user_id)
    return user_schema.jsonify(user)

@app.route('/users/', methods=['POST'])
def create_user():
    name = request.json.get('name', '')
    display_email = request.json.get('display_email', '')
    picture_url = request.json.get('picture_url', '')
    about = request.json.get('about', '')
    zipcode = request.json.get('zipcode', '')
    user = User(name=name, display_email=display_email, picture_url=picture_url, about=about, zipcode=zipcode)

    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/instruments/', methods=['POST'])
def create_instrument():
    name = request.json.get('name', '')
    instrument = Instrument(name=name)

    db.session.add(instrument)
    db.session.commit()
    return instrument_schema.jsonify(instrument)



from app import routes
