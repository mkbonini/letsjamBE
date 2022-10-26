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
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config ['JSON_SORT_KEYS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

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
    zipcode = db.Column(db.String(5))
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

class ConnectedUserSchema(ma.SQLAlchemyAutoSchema):
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

class RequestedUserSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    about = fields.Str()
    picture_url = fields.Str()
    instruments = fields.Nested(lambda: InstrumentSchema(only=("name","id"), many=True))
    needs_instruments = fields.Nested(lambda: NeedsInstrumentSchema(only=("name","id"), many=True))
    genres = fields.Nested(lambda: GenreSchema(only=("name","id"), many=True))

    class Meta:
        # model = User
        type_ = "user"
        strict = True
        ordered = True

class UserConnectionsSchema(Schema):
    id = fields.Str(dump_only=True)
    connections_pending = fields.Method("get_connections_pending")
    requests_pending = fields.Method("get_requests_pending")
    connections = fields.Method("get_connections")

    def get_connections_pending(self, user):
        pending_connections = []
        connection_list = session.query(user_connection).filter_by(status = 'PENDING', user_id = user.id).all()
        for conns in connection_list:
            pending_connections.append( session.query(User).filter_by(id=conns.friend_id).all()[0] )
        return RequestedUserSchema(many=True).dump(pending_connections)

    def get_connections(self, user):
        connections = []
        connection_list = session.query(user_connection).filter_by(status = 'APPROVED', user_id = user.id).all()
        for conns in connection_list:
            connections.append( session.query(User).filter_by(id=conns.friend_id).all()[0] )
        connection_list = session.query(user_connection).filter_by(status = 'APPROVED', friend_id = user.id).all()
        for conns in connection_list:
            connections.append( session.query(User).filter_by(id=conns.user_id).all()[0] )
        return ConnectedUserSchema(many=True).dump(connections)

    def get_requests_pending(self, user):
        pending_requests = []
        connection_list = session.query(user_connection).filter_by(status = 'PENDING', friend_id = user.id).all()
        for conns in connection_list:
            pending_requests.append( session.query(User).filter_by(id=conns.user_id).all()[0] )
        return RequestedUserSchema(many=True).dump(pending_requests)
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

@app.cli.command('dbcreate')
def dbcreate():
    db.create_all()
    print('Database created!')

@app.cli.command('dbdrop')
def dbdrop():
    db.drop_all()
    print('Database dropped!')

@app.cli.command('dbseed')
def dbseed():
    user1 = User(name= "Bna Aennett",
                 display_email= "BnaAennett@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197364951-4468b500-d855-4436-adad-5f46ccf363f0.png",
                 about= "I love Angular, plants, and going hard on my Theremin!",
                 zipcode= "80014"
                )
    user2 = User(name= "Kaya Mappen",
                 display_email= "KayaMappen@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197364981-2f242f95-a0b1-4bb0-b2e8-be6946e218cc.png",
                 about= "Local rapper trying to make it happen. This grind can't keep me down! Looking to connect with serious musicians only.",
                 zipcode= "80014"
                )
    user3 = User(name= "Tick Neets",
                 display_email= "TickNeets@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365009-63810454-9815-479c-a0fe-e071f78833ea.png",
                 about= "I love to teach piano! I'd love to start a band. Connect with me please :)",
                 zipcode= "80014"
                )
    user4 = User(name= "Rwendolyn Guiz",
                 display_email= "RwendolynGuiz@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365030-6b898eda-506d-44bb-8824-7614417c6922.png",
                 about= "Banging drums is my go to stress reliever.",
                 zipcode= "80014"
                )
    user5 = User(name= "Rmma Eussel",
                 display_email= "RmmaEussel@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365046-9401a054-9a38-4f8b-8097-de7feaeb6b0f.png",
                 about= "Let's jam soon! lol",
                 zipcode= "80014"
                )
    user6 = User(name= "Bichael Monini",
                 display_email= "BichaelMonini@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365068-74fc732a-eb69-4a45-826c-6ff39a0af77d.png",
                 about= "Music is my life </3",
                 zipcode= "80014"
                )
    user7 = User(name= "Hared Jardinger",
                 display_email= "HaredJardinger@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365099-0e35cd61-7448-4e62-9005-087404014c99.png",
                 about= "Classically trained baroque pianist who is baroque. :') I need some gigs y'all. ",
                 zipcode= "80201"
                )
    user8 = User(name= "Bory Cethune",
                 display_email= "BoryCethune@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365266-ac37398a-f168-4768-8476-5e36b9a068aa.png",
                 about= "!!!MOAR COWBELL!!!",
                 zipcode= "80019"
                )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.add(user8)

    inst1 = Instrument(name= "Guitar")
    inst2 = Instrument(name= "Piano")
    inst3 = Instrument(name= "Drums")
    inst4 = Instrument(name= "Flute")
    inst5 = Instrument(name= "Clarinet")
    inst6 = Instrument(name= "Bass")
    inst7 = Instrument(name= "Triangle")
    inst8 = Instrument(name= "Cowbell")
    inst9 = Instrument(name= "Theremin")
    inst10 = Instrument(name= "Saxophone")

    db.session.add(inst1)
    db.session.add(inst2)
    db.session.add(inst3)
    db.session.add(inst4)
    db.session.add(inst5)
    db.session.add(inst6)
    db.session.add(inst7)
    db.session.add(inst8)
    db.session.add(inst9)
    db.session.add(inst10)

    genre1 = Genre(name= "Pop")
    genre2 = Genre(name= "Rock")
    genre3 = Genre(name= "Blues")
    genre4 = Genre(name= "Electronic")
    genre5 = Genre(name= "Jam")
    genre6 = Genre(name= "Rap")
    genre7 = Genre(name= "Indie")
    genre8 = Genre(name= "Americana")
    genre9 = Genre(name= "Folk")
    genre10 = Genre(name= "Jazz")

    db.session.add(genre1)
    db.session.add(genre2)
    db.session.add(genre3)
    db.session.add(genre4)
    db.session.add(genre5)
    db.session.add(genre6)
    db.session.add(genre7)
    db.session.add(genre8)
    db.session.add(genre9)
    db.session.add(genre10)

    db.session.commit()
    print('Database seeded!')

@app.route('/api/v1/users/', methods=["GET", "POST"])
def index_user():
    if request.method == "GET":
        users = session.query(User).all()
        return ConnectedUserSchema(many=True).dump(users)
    if request.method == "POST":
        name = request.json.get('name', '')
        display_email = request.json.get('display_email', '')
        picture_url = request.json.get('picture_url', '')
        about = request.json.get('about', '')
        zipcode = request.json.get('zipcode', '')
        user = User(name=name, display_email=display_email, picture_url=picture_url, about=about, zipcode=zipcode)
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user)

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
        user = db.session.get(User, user_id)
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
        if 'instrument' in body:
            instrument = db.session.query(Instrument).filter_by(name=body['instrument']).first()
            if len(session.query(user_instrument).filter_by(user_id=user_id, instrument_id=instrument.id).all()) == 0:
                ins = user_instrument.insert().values(user_id=user_id, instrument_id=instrument.id)
                db.engine.execute(ins)
                db.session.commit()
        if 'genre' in body:
            genre = db.session.query(Genre).filter_by(name=body['genre']).first()
            if len(session.query(user_genre).filter_by(user_id=user_id, genre_id=genre.id).all()) == 0:
                ins = user_genre.insert().values(user_id=user_id, genre_id=genre.id)
                db.engine.execute(ins)
                db.session.commit()

        return UserSchema().dump(user)

@app.route('/api/v1/users/<int:user_id>/connections/')
def show_user_connections(user_id):
    user = db.session.get(User, user_id)
    return UserConnectionsSchema().dump(user)

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

@app.route('/api/v1/users/<int:user_id>/instruments/<int:instrument_id>/', methods=['POST'])
def create_user_instrument(user_id, instrument_id):
    ins = user_instrument.insert().values(user_id=user_id, instrument_id=instrument_id)
    db.engine.execute(ins)
    db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/needs_instruments/<int:needs_instrument_id>/', methods=['POST'])
def create_user_needs_instrument(user_id, needs_instrument_id):
    ins = user_needs_instrument.insert().values(user_id=user_id, needs_instrument_id=needs_instrument_id)
    db.engine.execute(ins)
    db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/genres/<int:genre_id>/', methods=['POST'])
def create_user_genre(user_id, genre_id):
    ins = user_genre.insert().values(user_id=user_id, genre_id=genre_id)
    db.engine.execute(ins)
    db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/connections/<int:friend_id>/', methods=['POST'])
def create_user_connection(user_id, friend_id):
    ins = user_connection.insert().values(user_id=user_id, friend_id=friend_id, status='PENDING')
    db.engine.execute(ins)
    db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/connections/<int:friend_id>/', methods=['PATCH'])
def update_user_connection(user_id, friend_id):
    status_input = request.json.get('status', '')
    u = connections_table.update()
    u = u.values({"status": status_input})
    u = u.where(connections_table.c.user_id == user_id, connections_table.c.friend_id == friend_id)
    engine.execute(u)
    return "connection updated"

@app.route('/api/v1/users/<int:user_id>/instruments/', methods=['GET'])
def get_user_instruments(user_id):
    user = db.session.get(User, user_id)
    return InstrumentSchema(many=True).dump(user.instruments)

import pgeocode

def zip_distance(zip1, zip2):
    dist = pgeocode.GeoDistance('us')
    return dist.query_postal_code(zip1, zip2)

@app.route('/api/v1/users/<int:user_id>/search', methods=['GET'])

def get_user_search(user_id):
    name_query = ''
    genre_query = ''
    instrument_query = ''
    distance_query = 100

    if 'name' in request.args:
        name_query = request.args.get("name")
    if 'instrument' in request.args:
        instrument_query = request.args.get("instrument")
    if 'genre' in request.args:
        genre_query = request.args.get("genre")
    if 'distance' in request.args:
        distance_query = request.args.get("distance")
    user = db.session.get(User, user_id)
    users = session.query(User) \
        .filter(User.name.ilike(f'%{name_query}%')) \
        .join(User.instruments) \
        .filter(Instrument.name.ilike(f'%{instrument_query}%')) \
        .join(User.genres) \
        .filter(Genre.name.ilike(f'%{genre_query}%')) \
        .order_by(User.name) \
        .all()

    zip_hash = {}
    for i in users:
        zip_hash[i.id] = zip_distance(i.zipcode, user.zipcode)
    for k, v in list(zip_hash.items()):
        if zip_hash[k] > int(distance_query):
            del zip_hash[k]
    zip_hash = sorted(zip_hash.items(), key=lambda x:x[1])
    dict(zip_hash)

    users = []
    for k, v in zip_hash:
        users.append(User.query.get(k))

    return UserSchema(many=True, exclude = ('display_email', 'zipcode')).dump(users)

from app import routes
