from flask import make_response, render_template, current_app, jsonify
from flask_restful import Resource, reqparse
from util.userAuth import auth_required

from schema.DataSet import DataSet

from schema.User import User
from schema.Query import Query
from schema.Assignment import Assignment

parser = reqparse.RequestParser()
parser.add_argument('instructor', type=str)
parser.add_argument('class', type=str)
parser.add_argument('dataset', type=str)
parser.add_argument('query', type=str)
parser.add_argument('ranker', type=str)
parser.add_argument('params', type=dict)
parser.add_argument('status', type=bool)
parser.add_argument('content', type=str)
parser.add_argument('creator', type=str)


class AssignmentAPI(Resource):
    @auth_required
    def get(self):
        name_dict = {}
        dataset = {}
        for i in User.objects:
            if i.group == 1:
                name_dict[i.id] = i.name
        for i in DataSet.objects:
            dataset[i.id] = i.ds_name


    def post(self):
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        query = args['query']
        ranker = args['ranker']
        params = args['params']
        dataset = args['dataset']
        class_ = args['class']
        instructor = args['instructor']

        instructor = User.objects(id=instructor)
        class_ = Class.objects(id=class_)
        dataset = DataSet.objects(id=dataset)

        # serialize params
        serialized_params = ""
        for key in params:
            value = params[key]
            serialized_params += key + ":" + value + ","
        serialized_params = serialized_params[:-1]

        # add assignment to each student in class
        annotators = User.objects(class_=class_)

        for annotator in annotators:
            assignment = Assignment()
            assignment.query = query
            assignment.instructor = instructor
            assignment.annotator = annotator
            assignment.ranker = ranker
            assignment.params = params
            assignment.dataset = dataset
            assignment.status = False
            assignment.view_status = False
            assignment.save()

            
        return make_response(jsonify("succeed"), 200, headers)


class AddQueryAPI(Resource):
    def post(self):
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        content = args['content']
        dataset = args['dataset']
        creator = args['creator']
        dataset = DataSet.objects(id=dataset)
        creator = User.objects(id=creator)
        query = Query()
        query.content = content
        query.data_set = dataset[0]
        query.creator = creator[0]
        query.save()
        return make_response(jsonify("succeed"), 200, headers)
