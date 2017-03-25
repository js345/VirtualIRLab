from flask import make_response, render_template
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)
parser.add_argument('data_set', type=str)
parser.add_argument('ranker', type=str)


class SearchAPI(Resource):

    def get(self, ds_name):
        args = parser.parse_args()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)

    def post(self, ds_name):
        args = parser.parse_args()
        pass