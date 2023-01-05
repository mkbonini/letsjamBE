from flask import Flask, request, session
import enum
from datetime import datetime
import os
import pgeocode
import json
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
app.config

basedir = os.path.abspath(os.path.dirname(__file__))
# db_uri = "postgresql://postgres:2npp51WDpjnxMdi@lets-jam-db.internal:5432"
db_uri = "postgresql://postgres:2npp51WDpjnxMdi@lets-jam-db.fly.dev:5432"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
ma = Marshmallow(app)

engine = create_engine(db_uri, pool_pre_ping=True)
metadata = MetaData(engine)
metadata.reflect()
connections_table = metadata.tables["user_connection"]
Session = sessionmaker(bind=engine)
session = Session()

from app.models import *
try:
  from app.schemas import *
  from app.routes import *
  from app import routes
  from app import seeds
  session.commit()
except:
  session.rollback()
  raise
    
