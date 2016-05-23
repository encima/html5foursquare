import os
from app import db, app
from flask import url_for
import flask.ext.login as flask_login
from datetime import datetime


class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    sq_access_token = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(300))

    def __init__(self, email, p_hash):
        self.email = email
        self.password_hash = p_hash
        self.sq_access_token = None

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r %r>' % (self.email, self.id)
