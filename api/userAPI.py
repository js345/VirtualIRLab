from flask import abort
from flask_restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from schema.User import User
from schema import redis_store
from util.userAuth import auth_required
from util.exception import InvalidUsage


userParser = reqparse.RequestParser()
userParser.add_argument('name', type=str)
userParser.add_argument('password', type=str)
userParser.add_argument('email', type=str)
userParser.add_argument('group', type=int)

class UserAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        name = args['name']
        email = args['email']
        group = args['group']
        password = args['password']
        if email is None or password is None:
            abort(400)

        user = User(name=name, email=email, group=group)
        user.hash_password(password)
        try:
            user.save()
        except ValidationError as e:
            raise InvalidUsage(e.message)
        except NotUniqueError as e:
            raise InvalidUsage("The user name or email has been used. Please use another user name.")

        token = user.generate_auth_token()
        redis_store.set(str(user.id), token)

        return ({'status': 'success', 'message': 'You have successfully created an account!'}, 201)


class LoginAPI(Resource):
    @auth_required
    def get(self, user_id):
        user = User.objects(id=user_id).first()
        token = user.generate_auth_token()
        redis_store.set(user_id, token)
        return {'token': token}

    def post(self):
        args = userParser.parse_args()
        email = args['email']
        password = args['password']
        if email is None or password is None:
            abort(400)

        user = User.objects(email=email).first()

        if not user or not user.check_password(password):
            raise InvalidUsage('Email and password do not match')
        token = user.generate_auth_token()
        redis_store.set(str(user.id), token)
        return {'token': token.decode('utf8')}