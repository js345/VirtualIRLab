from flask import abort,make_response, render_template, current_app, jsonify, request
from flask_restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from schema.User import User
# from schema.Profile import Profile
from schema import redis_store
from util.userAuth import auth_required
# from util.emails import send_activate_account_email
from util.exception import InvalidUsage
# from api.rongcloudAPI import rongcloudToken


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
        # profile = Profile(user=user)
        try:
            user.save()
            # profile.save()
        except ValidationError as e:
            raise InvalidUsage(e.message)
        except NotUniqueError as e:
            raise InvalidUsage("The user name or email has been used. Please use another user name.")

        token = user.generate_auth_token()
        redis_store.set(str(user.id), token)
        # send_activate_account_email(email,token)

        return ({'status': 'success', 'message': 'You have successfully created an account!'}, 201)


class LoginAPI(Resource):
    # renew token by using old valid token
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
        # if not user.is_activated:
        #     raise InvalidUsage('Account not activated')

        # profile = Profile.objects(user=user.id).first()

        # rongToken = rongcloudToken(profile.id)
        token = user.generate_auth_token()
        redis_store.set(str(user.id), token)
        return {'token': token}




#
# activateAccountParser = reqparse.RequestParser()
# activateAccountParser.add_argument('token', type=str)
# class ActivateAPI(Resource):
#     def get(self):
#         args = activateAccountParser.parse_args()
#         token = args['token']
#         if token is None:
#             abort()
#
#         user_id = load_token(token)
#         user = User.objects(id=user_id).first()
#         if user is None:
#             abort(400)
#         user.is_activated = True
#         user.save()
#
#         return "Your account has been activated!"