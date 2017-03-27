from flask import make_response, render_template, current_app, jsonify
from flask_restful import Resource, reqparse

from schema.DataSet import DataSet

from search.searcher import Searcher

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)
parser.add_argument('ranker', type=str)
parser.add_argument('num_results', type=int)
parser.add_argument('params', type=dict)


class SearchAPI(Resource):

    def get(self, author, ds_name):
        args = parser.parse_args()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)

    def post(self, author, ds_name):
        args = parser.parse_args()
        query = args['query']
        ranker = args['ranker']
        num_results = args['num_results']
        params = args['params']
        # To do: check for invalid access here
        # ds = DataSet.objects(author=author, ds_name=ds_name)

        path = current_app.root_path + "/data/" + author
        searcher = Searcher(author, ds_name, path)
        return jsonify(searcher.search(query, ranker, params, num_results))
