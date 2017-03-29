from flask import make_response, render_template, current_app, jsonify, request
from flask_restful import Resource, reqparse

from schema.Annotation import Annotation

parser = reqparse.RequestParser()
parser.add_argument('User', type=str)
parser.add_argument('DataSet', type=str)
parser.add_argument('Query', type=str)
parser.add_argument('doc', type=dict, action="append")


class AnnotationAPI(Resource):

    def post(self):
        args = parser.parse_args()
        query = args['Query']
        user = args['User']
        DataSet = args['DataSet']
        doc = args['doc']
        headers = {'Content-Type': 'application/json'}
        return make_response(jsonify("succeed"), 200, headers)
