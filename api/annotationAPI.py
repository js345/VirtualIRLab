from flask import make_response, render_template, current_app, jsonify, request
from flask_restful import Resource, reqparse

from schema.Annotation import Annotation
from schema.User import User
from schema.DataSet import DataSet
from schema.Query import Query

parser = reqparse.RequestParser()
parser.add_argument('user', type=str)
parser.add_argument('dataSet', type=str)
parser.add_argument('query', type=str)
parser.add_argument('doc', type=dict, action="append")


class AnnotationAPI(Resource):

    def post(self):
        args = parser.parse_args()
        print(args)
        query = args['query']
        user = args['user']
        data_id = args['dataSet']
        doc = args['doc']
        headers = {'Content-Type': 'application/json'}
        annotator = User.objects(name = user)
        ds = DataSet.objects(ds_name = data_id)
        print(data_id)
        print(ds)
        #q_id = Query.objects(id = query)
        for pair in doc:
            annotation = Annotation()
            annotation.annotator = annotator[0]
            #annotation.query = q_id
            annotation.data_set = ds[0]
            annotation.doc = pair['doc_id']
            annotation.judgement = bool(pair['judge'])
            annotation.save()
        return make_response(jsonify("succeed"), 200, headers)
