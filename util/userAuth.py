from flask import abort, current_app, request, session, redirect, render_template, make_response
from schema import redis_store
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from functools import wraps
from schema.User import User

def login_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = {'Content-Type': 'text/html'}
        try:
            token = session['token']
        except:
            print("Cannot find token")
            return make_response(render_template("index.html"),200,headers)

        if token is None:
            print("Token is null")
            return make_response(render_template("index.html"),200,headers)

        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            user_id = s.loads(token)
        except SignatureExpired:
            return make_response(render_template("index.html"),200,headers)    # valid token, but expired
        except BadSignature:
            return make_response(render_template("index.html"),200,headers)    # invalid token

        user = User.objects(id=user_id).first()

        if redis_store.get(user_id) == token:
            return f(*args, **kwargs)
        else:
            return make_response(render_template("index.html"),200,headers) 

    return decorated_function


def instructor_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = {'Content-Type': 'text/html'}
        s = Serializer(current_app.config.get('SECRET_KEY'))
        token = session['token']
        user_id = s.loads(token)
        user = User.objects(id=user_id).first()

        if user.group != "instructor":
            return make_response(render_template("index.html"),200,headers)

        return f(*args, **kwargs)

    return decorated_function


def annotator_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = {'Content-Type': 'text/html'}
        s = Serializer(current_app.config.get('SECRET_KEY'))
        token = session['token']
        user_id = s.loads(token)
        user = User.objects(id=user_id).first()

        if user.group != "annotator":
            return make_response(render_template("index.html"),200,headers)

        return f(*args, **kwargs)

    return decorated_function
