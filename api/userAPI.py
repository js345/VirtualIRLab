from flask import redirect, url_for
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
            return {'message': 'New account registered!'}, 200
        except ValidationError:
            return {'message': 'Validation failed!'}, 400
        except NotUniqueError:
            return {'message': 'Account already registered!'}, 400


class LoginAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        user = User.objects(email=args['email']).first()
        if not user:
            return {'message': 'Invalide email!'}, 404
        if not user.check_password(args['password']):
            return {'message': 'Wrong password!'}, 404
        login_user(user)
        return {'role': user.role}, 200


class LogoutAPI(Resource):
    @login_required
    def post(self):
        logout_user()
        return redirect(url_for('main'))
