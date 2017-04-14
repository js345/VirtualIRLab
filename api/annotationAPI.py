from flask import make_response, render_template, current_app, jsonify, request
from flask_restful import Resource, reqparse

from schema.Annotation import Annotation
from schema.User import User
from schema.DataSet import DataSet
from schema.Query import Query
import json
parser = reqparse.RequestParser()
parser.add_argument('user', type=str)
parser.add_argument('dataset', type=str)
#parser.add_argument('Query', type=str)
parser.add_argument('doc', type=str)


class AnnotationAPI(Resource):
    def serialize(self, docs):
        docs = docs.split(";")
        documents = []

        for doc in docs:
            params = doc.split(",")
            document = {}
            for param in params:
                key_value = param.split(":")
                document[key_value[0]] = key_value[1]
            documents.append(document)

        return documents

    def post(self):
        
        args = parser.parse_args()
        #query = args['query']
        user = args['user']
        data_id = args['dataset']
        documents = self.serialize(args['doc'])

        headers = {'Content-Type': 'application/json'}
        annotator = User.objects(name = user)
        ds = DataSet.objects(ds_name = data_id)
 
        #q_id = Query.objects(id = query)
        for pair in documents:
            annotation = Annotation()
            annotation.annotator = annotator[0]
            #annotation.query = q_id
            annotation.data_set = ds[0]
            annotation.doc = pair['doc_id']
            annotation.judgement = (pair['judge'] == "true")
            annotation.save()

        return make_response(jsonify("succeed"), 200, headers)
