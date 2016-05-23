import os
from flask import Flask, request, redirect, url_for, render_template, g
from flask_sqlalchemy import SQLAlchemy
import flask.ext.login as flask_login
import foursquare

app = Flask(__name__)
app.config.from_pyfile('ol.cfg', silent=True)
app.client = foursquare.Foursquare(client_id=app.config['SQ_CLIENT_ID'], client_secret=app.config['SQ_CLIENT_SECRET'], redirect_uri='http://gwillia.ms')
db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

from app import views, models

db.create_all()
