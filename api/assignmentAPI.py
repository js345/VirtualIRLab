from flask import make_response, render_template, session, jsonify
from flask_restful import Resource, reqparse
from schema.DataSet import DataSet

from schema.User import User
from schema.Query import Query
from schema.Class import Class
from schema.Assignment import Assignment


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('instructor_id', type=str)
parser.add_argument('class', type=str)
parser.add_argument('dataset', type=str)
parser.add_argument('query', type=str)
parser.add_argument('ranker', type=str)
parser.add_argument('params', type=dict)
parser.add_argument('deadline', type=str)
parser.add_argument('status', type=bool)
parser.add_argument('content', type=str)
parser.add_argument('creator', type=str)


class AssignAPI(Resource):
    # instructor post new assignment
    def post(self):
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        name = args['name']
        query = args['query']
        ranker = args['ranker']
        params = args['params']
        dataset = args['dataset']
        deadline = args['deadline']
        # class_ = args['class']
        instructor_id = session['user_id']

        instructor = User.objects(id=instructor_id).first()
        # class_ = Class.objects(id=class_)
        dataset = DataSet.objects(id=dataset).first()

        # serialize params
        serialized_params = ""
        for key in params:
            value = params[key]
            serialized_params += key + ":" + value + ","
        serialized_params = serialized_params[:-1]

        # add assignment to each student in class

        # send assignments to all annotators by default(test)
        annotators = User.objects(group='annotator')

        for annotator in annotators:
            assignment = Assignment()
            assignment.name = name
            assignment.query = query
            assignment.instructor = instructor
            assignment.annotator = annotator
            assignment.ranker = ranker
            assignment.params = serialized_params
            assignment.dataset = dataset
            assignment.deadline = deadline
            assignment.status = False
            assignment.view_status = False
            assignment.save()

            
        return make_response(jsonify("succeed"), 200, headers)



class AssignmentAPI(Resource):
    def get(self, instructor_name, assignment_name):
        headers = {'Content-Type': 'text/html'}
        args = parser.parse_args()
        instructor = User.objects(name=instructor_name).first()
        user_id = session['user_id']
        user = User.objects(id=user_id).first()

        assignment = Assignment.objects(name=assignment_name)  \
            .filter(instructor=instructor)  \
            .filter(annotator=user).first()

        assignment.instructor_name = assignment.instructor.name
        assignment.ds_name = assignment.dataset.name

        return make_response(
            render_template(
                "assignment.html",
                assignment = assignment
            ),
            200,headers)



class AssignmentUpdateAPI(Resource):
    def get(self):
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()

        name = args['name']

        assignment = Assignment.objects(name=name).first()

        return jsonify(assignment)



    # def post(self):


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
