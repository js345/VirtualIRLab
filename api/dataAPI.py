from flask import make_response, jsonify
from flask_restful import Resource, reqparse


parser = reqparse.RequestParser()
parser.add_argument('author', type=str)
parser.add_argument('ds_name', type=str)


class DataAPI(Resource):

    def post(self):
        headers = {'Content-Type': 'application/json'}
        return make_response(jsonify({}), 200, headers)
