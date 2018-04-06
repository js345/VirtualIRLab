from flask import redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from flask_restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError

from schema.User import User

userParser = reqparse.RequestParser()
userParser.add_argument('name', type=str)
userParser.add_argument('password', type=str)
userParser.add_argument('email', type=str)
userParser.add_argument('role', type=str)


class RegisterAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        try:
            User(args['name'], args['email'], args['role'], User.hash_password(args['password'])).save()
            msg = 'New account registered!'
        except ValidationError:
            msg = 'Validation failed!'
        except NotUniqueError:
            msg = 'Account already registered!'
        flash(msg)
        return redirect(url_for('main'))


class LoginAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        user = User.objects(email=args['email']).first()
        if not user:
            flash('Invalid Email')
            return redirect(url_for('main'))
        if not user.check_password(args['password']):
            flash('Wrong Password')
            return redirect(url_for('main'))
        login_user(user)
        return redirect(url_for(user.role + 'api'))


class LogoutAPI(Resource):
    @login_required
    def post(self):
        logout_user()
        flash('Log out')
        return redirect(url_for('main'))
