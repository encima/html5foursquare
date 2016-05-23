import os
from app import app, db, login_manager, models
from app.models import User
from passlib.hash import sha256_crypt
from flask import Flask, request, redirect, url_for, render_template, g, send_from_directory, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import flask.ext.login as flask_login
from werkzeug import secure_filename
from datetime import datetime
import foursquare


@login_manager.user_loader
def user_loader(id):
     return User.query.get(int(id))


@login_manager.request_loader
def request_loader(request):
    users = models.User.query.all()
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Login Handling

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('posted')
        email = request.form['email']
        pwd = request.form['password']
        p_hash = sha256_crypt.encrypt(pwd, rounds=200000, salt_size=16)
        user = models.User(email, p_hash)
        db.session.add(user)
        db.session.commit()
        flask_login.login_user(user)
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.form)
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        print(pwd)
        user = models.User.query.filter_by(email=email).first()
        print(user)
        if user is not None and sha256_crypt.verify(pwd, user.password_hash):
            flask_login.login_user(user)
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

@app.route('/auth/foursquare', methods=['POST'])
@flask_login.login_required
def auth_foursquare():
    code = request.form['code']
    access_token = app.client.oauth.get_token(code)
    flask_login.current_user.sq_access_token = access_token
    db.session.add(flask_login.current_user)
    db.session.commit()
    print(flask_login.current_user.sq_access_token)
    return redirect(url_for('index'))
# END Login Handling

# Post Handling

@app.route('/api/venues', methods=['POST'])
def get_venues():
    print(request)
    places = app.client.venues.search(params={'ll': request.form['ll']})
    return jsonify(places)

@app.route('/api/checkin', methods=['POST'])
def checkin():
    print(request.form['id'])
    response = app.client.checkins.add(params={'venueId': request.form['id'], 'll': request.form['ll']})
    flash('Successfully Checked In!', 'success')
    return jsonify(response)

@app.route('/')
@flask_login.login_required
def index(name=None):
    places = []
    if flask_login.current_user.sq_access_token is not None:
        app.client = foursquare.Foursquare(access_token=flask_login.current_user.sq_access_token)

    return render_template('index.html', user=flask_login.current_user, places=places)
