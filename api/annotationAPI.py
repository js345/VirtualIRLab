from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from schema.Annotation import Annotation
from schema.DataSet import DataSet
from schema.Query import Query
from schema.User import User

parser = reqparse.RequestParser()
parser.add_argument('user', type=str)
parser.add_argument('dataset', type=str)
parser.add_argument('query', type=str)
parser.add_argument('doc', type=dict, action="append")


class AnnotationAPI(Resource):
    def post(self):
        args = parser.parse_args()
        query = args['query']
        user = args['user']
        data_id = args['dataset']
        doc = args['doc']
        headers = {'Content-Type': 'application/json'}
        annotator = User.objects(id=user)
        ds = DataSet.objects(id=data_id)
        q_id = Query.objects(id=query)
        for pair in doc:
            annotation = Annotation()
            annotation.annotator = annotator[0]
            annotation.query = q_id[0]
            annotation.data_set = ds[0]
            annotation.doc = pair['doc_id']
            annotation.judgement = (pair['judge'] == "true")
            annotation.save()

        return make_response(jsonify("succeed"), 200, headers)
