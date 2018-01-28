from flask import make_response, render_template, current_app, jsonify
from flask_restful import Resource, reqparse

from schema.Query import Query
from schema.Assignment import Assignment
from schema.User import User

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)
parser.add_argument('user_id', type=str)
parser.add_argument('assignment_id', type=str)
parser.add_argument('doc_scores', type=dict)

class QueryAPI(Resource):
	def post(self):
		args = parser.parse_args()

		query_content = args['query']
		assignment_id = args['assignment_id']
		user_id = args['user_id']
		doc_scores = args['doc_scores']

		assignment = Assignment.objects(id=assignment_id).first()
		creator = User.objects(id=user_id).first()

		query = Query()
		query.content = query_content
		query.assignment = assignment
		query.doc_scores = doc_scores
		query.creator = creator
		query.save()

		return "OK"

		