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
parser.add_argument('assignment', type=dict)
parser.add_argument('annotations', type=dict)


class AnnotationAPI(Resource):

    def post(self): 
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        assignment = args['assignment']
        assignment_id = assignment["_id"]["$oid"]
        assignment = Assignment.objects(id=assignment_id).first()
        annotations = args['annotations']
        user_id = session['user_id']

        annotator = User.objects(id=user_id).first()


        for file_name in annotations:
            label = annotations[file_name]

            dataset = assignment.dataset

            document = Document.objects(dataset=dataset) \
                        .filter(name=file_name).first()


            if len(Annotation.objects(annotator=annotator,document=document,assignment=assignment)) != 0:
                a = Annotation.objects(annotator=annotator,document=document,assignment=assignment).first()
                a.modify(judgement=label)
            else:
                a = Annotation()
                a.annotator = annotator
                a.document = document
                a.judgement = label
                a.assignment = assignment
                a.save()

        #mark the assignment complete
        assignment.status = True
        assignment.save()

        return make_response(jsonify("succeed"), 200, headers)
