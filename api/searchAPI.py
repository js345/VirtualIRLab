from flask import redirect, url_for
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)
parser.add_argument('data_set', type=str)
parser.add_argument('ranker', type=str)


class SearchAPI(Resource):

    def get(self, ds_name):
        args = parser.parse_args()
        return redirect(url_for('static', filename='index.html'))

    def post(self, ds_name):
        args = parser.parse_args()
        pass