# 6B/19090113/Mulyana Putriyani
# 6D/19090083/Risma Niankupandang

#from crypt import methods
import os, random, string
from unittest import result
import uuid
from django.http import response
import jwt
import datetime
from flask import Flask
from flask import render_template
from flask import request, make_response
from flask import redirect
from flask import jsonify
import json 
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlparse import tokens
from werkzeug.security import generate_password_hash, check_password_hash

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "users.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')

class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)

db.create_all()

@app.route("/api/v1/login", methods=["POST"])
def login():
    dataUsername = request.form.get('username')
    dataPassword = request.form.get('password')
    reqq = dataUsername and dataPassword
    db.session.commit()

    if reqq :
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        User.query.update({'token': token})
        db.session.commit()

        return {'result': 'true', 'msg': 'Login berhasil!!', 'token': token}, 200
    else :
        return {'result': 'false', 'msg': 'Login gagal !!'}
 

@app.route('/api/v2/users/info', methods=["GET","POST"])
@auth.login_required
def info():
    token = request.values.get('token')
    akun = User.query.filter_by(token=token).first()
    if akun : 
        return akun.username
    else: 
        return False
if  __name__ == '__main__':  
     app.run(debug=True, port=5000)