from flask import redirect, session
from flask_restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError

from schema.User import User
from util.userAuth import login_auth_required

userParser = reqparse.RequestParser()
userParser.add_argument('name', type=str)
userParser.add_argument('password', type=str)
userParser.add_argument('email', type=str)
userParser.add_argument('role', type=str)


class UserAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        try:
            user = User(name=args['name'], email=args['email'], role=args['role'])
            user.hash_password(args['password'])
            user.save()
        except ValidationError:
            return {'message': 'Wrong value'}, 400
        except NotUniqueError:
            return {'message': 'The account is already registered!'}, 400
        return {'message': 'You have successfully created an account!'}, 201


class LoginAPI(Resource):
    @login_auth_required
    def get(self):
        # navigate user to right page
        user_id = session['user_id']
        user = User.objects(id=user_id).first()
        return redirect('/' + user.role)

    def post(self):
        args = userParser.parse_args()
        email = args['email']
        password = args['password']

        user = User.objects(email=email).first()
        if not user or not user.check_password(password):
            return {'state': 'failed', 'error': 'Email and password do not match'}

        # get token
        token = user.generate_auth_token()
        # store token to session
        session['token'] = token
        session['user_id'] = str(user.id)
        return {'state': 'success', 'role': user.role}
