# app/__init__.py: Flask application instance

from flask import Flask
import os
import enum
from flask import request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine, MetaData, Integer, ForeignKey, String, Column, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, sessionmaker
from marshmallow_jsonapi import fields, Schema

app = Flask(__name__)
app.config ['JSON_SORT_KEYS'] = False

basedir = os.path.abspath(os.path.dirname(__file__))
db_uri = "postgresql://mgdeiuhjogmlzz:0a44187da32e2c27267fa407dbd2e9370d19c5c00137900902273076c9f27737@ec2-44-209-24-62.compute-1.amazonaws.com:5432/d9e64hhn0dh9ou"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
ma = Marshmallow(app)

Base = declarative_base()
engine = create_engine(db_uri)
metadata = MetaData(engine)
metadata.reflect()
connections_table = metadata.tables["user_connection"]
Session = sessionmaker(bind=engine)
session = Session()

class ConnectionStatus(enum.Enum):
    APPROVED = "Approved"
    PENDING = "Pending"
    REJECTED = "Rejected"

class PlaysOrNeeds(enum.Enum):
    PLAYS = "Plays"
    NEEDS = "Needs"

user_instrument = db.Table('user_instrument',# Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('instrument_id', db.Integer, db.ForeignKey('instrument.id'), primary_key=True)
)

user_needs_instrument = db.Table('user_needs_instrument',#Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('needs_instrument_id', db.Integer, db.ForeignKey('needs_instrument.id'), primary_key=True)
)

user_genre = db.Table('user_genre',#Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

user_connection = db.Table('user_connection', #Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('status', db.Enum(ConnectionStatus))
)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    display_email = db.Column(db.String(255))
    picture_url = db.Column(db.String(255))
    about = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    instruments = db.relationship('Instrument', secondary=user_instrument,  lazy='select', backref=db.backref('users', lazy=True))
    needs_instruments = db.relationship('NeedsInstrument', secondary=user_needs_instrument,  lazy='joined', backref=db.backref('users', lazy=True))
    genres = db.relationship('Genre', secondary=user_genre, lazy='dynamic', backref=db.backref('users', lazy=True))
    connections = db.relationship('User', secondary=user_connection, primaryjoin=id == user_connection.c.user_id, secondaryjoin=id == user_connection.c.friend_id, lazy='dynamic', backref=db.backref('users', lazy=True))

    def __init__(self, name, display_email, picture_url, about, zipcode):
        self.name = name
        self.display_email = display_email
        self.picture_url = picture_url
        self.about = about
        self.zipcode = zipcode

class Instrument(db.Model):
    __tablename__ = "instrument"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

class NeedsInstrument(db.Model):
    __tablename__ = "needs_instrument"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name


class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name



class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    display_email = fields.Str()
    about = fields.Str()
    zipcode = fields.Str()
    picture_url = fields.Str()
    instruments = fields.Nested(lambda: InstrumentSchema(only=("name","id"), many=True))
    needs_instruments = fields.Nested(lambda: NeedsInstrumentSchema(only=("name","id"), many=True))
    genres = fields.Nested(lambda: GenreSchema(only=("name","id"), many=True))

    class Meta:
        # model = User
        type_ = "user"
        strict = True
        ordered = True

class InstrumentSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    class Meta:
        # model = Instrument
        type_ = "instrument"

class NeedsInstrumentSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    class Meta:
        type_ = "needs_instrument"

instrument_schema = InstrumentSchema()
instruments_schema = InstrumentSchema(many=True)


class UserInstrumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        table = user_instrument

user_instrument_schema = UserInstrumentSchema()

class GenreSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()

    class Meta:
        model = Genre

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

class UserConnectionsSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    class Meta:
        model = Genre

@app.route('/api/v1/users/<int:user_id>/', methods=["GET", "DELETE", "PATCH"])
def show_user(user_id):
    if request.method == "GET":
        user = db.session.get(User, user_id)
        return UserSchema().dump(user)

    if request.method == "DELETE":
        user = db.session.get(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return "User successfully deleted"

    if request.method == "PATCH":
        body = request.get_json()
        if 'name' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(name=body['name']))
            db.session.commit()
        if 'display_email' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(display_email=body['display_email']))
            db.session.commit()
        if 'picture_url' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(picture_url=body['picture_url']))
            db.session.commit()
        if 'about' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(about=body['about']))
            db.session.commit()
        if 'zipcode' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(zipcode=body['zipcode']))
            db.session.commit()
        return "User updated"

@app.route('/api/v1/users/<int:user_id>/connections')
def show_user_connections(user_id):
    user = db.session.get(User, user_id)
    pending_connections = []
    connections = []
    pending_requests = []
    connection_list = session.query(user_connection).filter_by(status = 'PENDING', user_id = user.id).all()
    for conns in connection_list:
        pending_connections.append( session.query(User).filter_by(id=conns.friend_id).all()[0] )
    connection_list = session.query(user_connection).filter_by(status = 'PENDING', friend_id = user.id).all()
    for conns in connection_list:
        pending_requests.append( session.query(User).filter_by(id=conns.user_id).all()[0] )
    connection_list = session.query(user_connection).filter_by(status = 'APPROVED', user_id = user.id).all()
    connection_list = connection_list + session.query(user_connection).filter_by(status = 'APPROVED', friend_id = user.id).all()
    for conns in connection_list:
        connections.append( session.query(User).filter_by(id=conns.friend_id).all()[0] )
    return UserSchema().dump(user)

@app.route('/api/v1/users/', methods=['POST'])
def create_user():
    name = request.json.get('name', '')
    display_email = request.json.get('display_email', '')
    picture_url = request.json.get('picture_url', '')
    about = request.json.get('about', '')
    zipcode = request.json.get('zipcode', '')
    user = User(name=name, display_email=display_email, picture_url=picture_url, about=about, zipcode=zipcode)
    db.session.add(user)
    db.session.commit()
    return UserSchema().dump(user)

@app.route('/api/v1/instruments/', methods=['POST'])
def create_instrument():
    name = request.json.get('name', '')
    instrument = Instrument(name=name)
    needs_instrument = NeedsInstrument(name=name)
    db.session.add(instrument)
    db.session.add(needs_instrument)
    db.session.commit()
    return instrument_schema.jsonify(instrument)

@app.route('/api/v1/genres/', methods=['POST'])
def create_genre():
    name = request.json.get('name', '')
    genre = Genre(name=name)

    db.session.add(genre)
    db.session.commit()
    return genre_schema.jsonify(genre)

@app.route('/api/v1/users/<int:user_id>/instruments/<int:instrument_id>', methods=['POST'])
def create_user_instrument(user_id, instrument_id):
    ins = user_instrument.insert().values(user_id=user_id, instrument_id=instrument_id)
    db.engine.execute(ins)
    db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/needs_instruments/<int:needs_instrument_id>', methods=['POST'])
def create_user_needs_instrument(user_id, needs_instrument_id):
    ins = user_needs_instrument.insert().values(user_id=user_id, needs_instrument_id=needs_instrument_id)
    db.engine.execute(ins)
    db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/genres/<int:genre_id>', methods=['POST'])
def create_user_genre(user_id, genre_id):
    ins = user_genre.insert().values(user_id=user_id, genre_id=genre_id)
    db.engine.execute(ins)
    db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/connections/<int:friend_id>', methods=['POST'])
def create_user_connection(user_id, friend_id):
    ins = user_connection.insert().values(user_id=user_id, friend_id=friend_id, status='PENDING')
    db.engine.execute(ins)
    db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/connections/<int:friend_id>', methods=['PATCH'])
def update_user_connection(user_id, friend_id):
    status_input = request.json.get('status', '')
    connection = session.query(user_connection).filter_by(user_id = user_id, friend_id = friend_id).all()[0]
    # connection.update({connection.status: status_input})
    user_connection.update().values(status=status_input).where(user_connection.c.user_id==user_id).where( user_connection.c.friend_id==friend_id    )
    # ins = user_connection.update().values(user_id=user_id, friend_id=friend_id, status=status)
    # db.engine.execute(ins)
    db.session.commit()
    return "connection updated"

@app.route('/api/v1/users/<int:user_id>/instruments', methods=['GET'])
def get_user_instruments(user_id):
    user = db.session.get(User, user_id)
    return InstrumentSchema(many=True).dump(user.instruments)


from app import routes
