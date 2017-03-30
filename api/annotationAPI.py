from flask import make_response, render_template, current_app, jsonify, request
from flask_restful import Resource, reqparse

from schema.Annotation import Annotation
from schema.User import User
from schema.DataSet import DataSet
from schema.Query import Query

parser = reqparse.RequestParser()
parser.add_argument('User', type=str)
parser.add_argument('DataSet', type=str)
parser.add_argument('Query', type=str)
parser.add_argument('doc', type=dict, action="append")


class AnnotationAPI(Resource):

    def post(self):
        args = parser.parse_args()
        query = args['Query']
        user = args['User']
        data_id = args['DataSet']
        doc = args['doc']
        headers = {'Content-Type': 'application/json'}
        annotator = User.objects(name = user)
        ds = DataSet.objects(ds_name = data_id)
        q_id = Query.objects(id = query)
        for pair in doc:
            annotation = Annotation()
            annotation.annotator = annotator
            annotation.query = q_id
            annotation.data_set = ds
            annotation.doc = pair['doc_id']
            annotation.judgement = bool(pair['judge'])
            annotation.save()

        return make_response(jsonify("succeed"), 200, headers)
