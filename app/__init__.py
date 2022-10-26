from flask import Flask, request, session
import enum
from datetime import datetime
import os
import pgeocode
from flask import request
from marshmallow_jsonapi import fields, Schema
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine, MetaData, Integer, ForeignKey, String, Column, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, sessionmaker
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

# Base = declarative_base()
engine = create_engine(db_uri)
metadata = MetaData(engine)
metadata.reflect()
connections_table = metadata.tables["user_connection"]
Session = sessionmaker(bind=engine)
session = Session()

from app import seeds
from app.models import *
from app.schemas import *
from app.routes import *
from app import routes
