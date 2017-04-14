from flask import make_response, render_template, current_app, jsonify
from flask_restful import Resource, reqparse

from schema.DataSet import DataSet

from search.searcher import Searcher

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)
parser.add_argument('ranker', type=str)
parser.add_argument('num_results', type=int)
parser.add_argument('params', type=str)


class SearchAPI(Resource):
    def serialize(self, params):
        ret = {}
        params = params.split(",")
        for param in params:
            key_value = param.split(":")
            ret[key_value[0]] = float(key_value[1])
        return ret

    def get(self, author, ds_name):
        args = parser.parse_args()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('search.html',documents={}), 200, headers)

    def post(self, author, ds_name):
        args = parser.parse_args()
        query = args['query']
        ranker = args['ranker']
        num_results = args['num_results']
        params = self.serialize(args['params'])
        headers = {'Content-Type': 'text/html'}
        print(params)

        path = current_app.root_path + "/data/" + author
        searcher = Searcher(author, ds_name, path)
        documents = jsonify(searcher.search(query, ranker, params, num_results))
        return make_response(documents)
