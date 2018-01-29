from flask import make_response, render_template, current_app, jsonify, request, session
from flask_restful import Resource, reqparse

from schema.Assignment import Assignment
from schema.Annotation import Annotation
from schema.User import User
from schema.DataSet import DataSet
from schema.Query import Query
from schema.Document import Document


import json
parser = reqparse.RequestParser()
parser.add_argument('assignment_id', type=str)
parser.add_argument('annotations', type=dict)


class AnnotationAPI(Resource):

    def post(self): 
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        assignment_id = args['assignment_id']
        assignment = Assignment.objects(id=assignment_id).first()

        annotations = args['annotations']
        user_id = session['user_id']

        annotator = User.objects(id=user_id).first()

        for query_content in annotations:
            query = Query.objects(assignment=assignment, content=query_content).first()

            apq = annotations[query_content]


            for file_name in apq:
                label = apq[file_name]

                dataset = assignment.dataset

                # print dataset.id
                # print file_name

                document = Document.objects(dataset=dataset) \
                            .filter(name=file_name).first()

                a = Annotation()
                a.annotator = annotator
                a.document = document
                a.judgement = label
                a.query = query
                a.save()

        #mark the assignment complete


        return make_response(jsonify("succeed"), 200, headers)
