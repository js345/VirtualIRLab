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
parser.add_argument('doc_scores', type=dict)


class AssignAPI(Resource):
    # instructor post new assignment
    def post(self):
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        name = args['name']
        ranker = args['ranker']
        params = args['params']
        dataset = args['dataset']
        deadline = args['deadline']
        doc_scores = args['doc_scores']
        # class_ = args['class']
        instructor_id = session['user_id']
 
        instructor = User.objects(id=instructor_id).first()
        # class_ = Class.objects(id=class_)
        dataset = DataSet.objects(id=dataset).first()

        # add assignment to each student in class

        # send assignments to all annotators by default(test)
        annotators = User.objects(group='annotator')

        statuses = dict()
        for annotator in annotators:
            statuses[str(annotator.id)] = False

        assignment = Assignment()
        assignment.name = name
        assignment.instructor = instructor
        assignment.ranker = ranker
        assignment.params = params
        assignment.dataset = dataset
        assignment.annotators = annotators
        assignment.statuses = statuses
        assignment.deadline = deadline
        assignment.save()

        # print assignment.id

            
        return str(assignment.id)



class AssignmentAPI(Resource):
    def get(self, instructor_name, assignment_name):
        headers = {'Content-Type': 'text/html'}
        args = parser.parse_args()
        instructor = User.objects(name=instructor_name).first()
        user_id = session['user_id']
        user = User.objects(id=user_id).first()

        assignment = Assignment.objects(name=assignment_name)  \
            .filter(instructor=instructor).first()

        assignment.instructor_name = assignment.instructor.name
        assignment.ds_name = assignment.dataset.ds_name
        assignment.ds_author = assignment.dataset.author.name

        queries = Query.objects(assignment=assignment)
        return make_response(
            render_template(
                "assignment.html",
                user = user,
                assignment = assignment,
                queries = queries
            ),
            200,headers)


parser.add_argument('assignment_id', type=str)

class AssignmentUpdateAPI(Resource):
    def post(self):
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        assignment_id = args['assignment_id']
        # print assignment_id

        assignment = Assignment.objects(id=assignment_id).first()

        name = args['name']
        query = args['query']
        ranker = args['ranker']
        params = args['params']
        dataset = args['dataset']
        deadline = args['deadline']
        doc_scores = args['doc_scores']

        assignments = Assignment.objects(instructor=assignment.instructor, name=assignment.name)

        for assignment in assignments:
            assignment.name = name
            assignment.query = query
            assignment.ranker = ranker
            assignment.params = params
            assignment.deadline = deadline

            if len(doc_scores) != 0:
                assignment.doc_scores = doc_scores
 
            assignment.save()

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
