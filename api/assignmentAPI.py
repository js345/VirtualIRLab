from flask import make_response, render_template, current_app, jsonify
from flask_restful import Resource, reqparse

from schema.DataSet import DataSet

from schema.User import User
from schema.Query import Query
from schema.Assignment import Assignment

parser = reqparse.RequestParser()
parser.add_argument('instructor', type=str)
parser.add_argument('annotator', type=str)
parser.add_argument('dataset', type=str)
parser.add_argument('query', type=str)
parser.add_argument('ranker', type=str)
parser.add_argument('params', type=dict)
parser.add_argument('status', type=bool)
parser.add_argument('content', type=str)
parser.add_argument('creator', type=str)


class AssignmentAPI(Resource):
    def post(self):
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        query = args['query']
        ranker = args['ranker']
        params = args['params']
        dataset = args['dataset']
        status = False
        annotator = args['annotator']
        instructor = args['instructor']
        instructor = User.objects(name=instructor)
        annotator = User.objects(name=annotator)
        query = Query.objects(content=query)
        dataset = DataSet.objects(ds_name=dataset)
        task = Assignment()
        task.query = query[0]
        task.ranker = ranker
        task.params = str(params)
        task.dataset = dataset[0]
        task.status = status
        task.annotator = annotator[0]
        task.instructor = instructor[0]
        task.save()
        return make_response(jsonify("succeed"), 200, headers)


class AddQueryAPI(Resource):
    def post(self):
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        content = args['content']
        dataset = args['dataset']
        creator = args['creator']
        dataset = DataSet.objects(ds_name=dataset)
        creator = User.objects(name=creator)
        query = Query()
        query.content = content
        query.data_set = dataset[0]
        query.creator = creator[0]
        query.save()
        return make_response(jsonify("succeed"), 200, headers)
