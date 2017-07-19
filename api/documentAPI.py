from flask import make_response, render_template, current_app, jsonify
from flask_restful import Resource, reqparse

from schema.User import User
from schema.DataSet import DataSet
from schema.Assignment import Assignment
from schema.Document import Document
from schema.Annotation import Annotation

parser = reqparse.RequestParser()

parser.add_argument('assignment_id', type=str)

# class DocumentsAPI(Resource):
#     def get(self):
        

class DocumentsAPI(Resource):

    def get(self):
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        assignment_id = args['assignment_id']

        documents = []

        assignment = Assignment.objects(id=assignment_id).first()
        assignments = Assignment.objects(instructor=assignment.instructor,name=assignment.name)
        
        doc_scores = assignment.doc_scores

        for doc_name in doc_scores:
            score = doc_scores[doc_name]
            full_doc_name = doc_name + ".txt"

            # get the document and count rel_num
            document = Document.objects(dataset=assignment.dataset,name=full_doc_name).first()

            rel_num = Annotation.objects(document=document,assignment__in=assignments,judgement='relevant').count()
            irrel_num = Annotation.objects(document=document,assignment__in=assignments,judgement='irrelevant').count()

            documents.append({
                'name' : full_doc_name,
                'score' : score,
                'rel_num' : rel_num,
                'irrel_num' : irrel_num
            })

        return make_response(jsonify(documents), 200, headers)



parser.add_argument("assignment", type=dict)
parser.add_argument("document_name", type=str)
class DocumentAPI(Resource):

    def post(self):
        args = parser.parse_args()

        assignment = args['assignment']
        document_name = args['document_name']

        dataset = DataSet.objects(id=assignment['dataset']['$oid']).first()

        ds_name = dataset.ds_name
        author_name = dataset.author.name

        doc_path = current_app.root_path + "/data/" + author_name + "/" + ds_name + "/" + document_name

        file = open(doc_path, "r")
        document = file.readlines()
        file.close()

        print document



