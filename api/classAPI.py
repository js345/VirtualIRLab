from flask import make_response, render_template, current_app, jsonify
from flask_restful import Resource, reqparse
from util.userAuth import auth_required
from schema.Class import Class
from schema.User import User

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('password', type=str)
parser.add_argument('instructor', type=str)

class ClassAPI(Resource):

        def post(self):
                headers = {'Content-Type': 'application/json'}
                args = parser.parse_args()
                instructor = args['instructor']
                name = args['name']
                password = args['password']

                class_ = Class()
                class_.instructor = instructor
                class_.name = name
                class_.password = password
                class_.save()