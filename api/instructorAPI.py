from flask import make_response, jsonify, current_app, request, render_template, session
from flask_restful import Resource, reqparse
from flask_paginate import Pagination, get_page_parameter


from schema.User import User
from schema.DataSet import DataSet
from schema.Class import Class
from schema.Assignment import Assignment
from schema.Annotation import Annotation
from schema.Document import Document
from schema.Query import Query

from schema import redis_store
from util.userAuth import login_auth_required, instructor_auth_required
from util.exception import InvalidUsage
import os,json

class InstructorAPI(Resource):

	@login_auth_required
	@instructor_auth_required
	def get(self):
		headers = {'Content-Type': 'text/html'}

		# get user
		user_id = session['user_id']
		user = User.objects(id=user_id).first()

		# generate new token
		token = user.generate_auth_token()
		redis_store.set(user_id, token)
		session['token'] = token

		# get all ds
		my_datasets = DataSet.objects(author=user)
		public_datasets = DataSet.objects(privacy='public', author__ne=user)
		authorized_datasets = DataSet.objects(privacy='private',collaborators__in=[user])
		
		# get all classes
		classes = []
		for class_ in Class.objects(instructor=user.name):
			classes.append(class_.name)

		# get all assignments
		assignments = []

		assignment_names = Assignment.objects(instructor=user).aggregate({
		    '$group': { '_id': '$name'}
		})

		assignment_names = list(assignment_names)

		# get all incomplete assignments
		incomplete_numbers = []

		for assignment_name in assignment_names:
			assignment_name = assignment_name['_id']

			assignment = Assignment.objects(name=assignment_name, instructor=user).first()

			# get judgements for each assignment
			ds_for_assignment = assignment.dataset
			docs_for_dataset = Document.objects(dataset=ds_for_assignment)

			incomplete_number = Assignment.objects(name=assignment_name,status=False).count()
			assignment['incomplete_number'] = incomplete_number
			assignment['id_'] = str(assignment['id'])
			assignment['ds_author'] = assignment.dataset.author.name
			assignment['ds_name'] = assignment.dataset.ds_name
			assignments.append(assignment)

			queries = Query.objects(assignment=assignment)
			assignment['queries'] = queries

		return make_response(render_template(
			"instructor.html", 
			data={
					"user" : json.dumps(user.to_json()),
					"my_datasets" : my_datasets,
					"public_datasets" : public_datasets,
					"authorized_datasets" : authorized_datasets,
					"classes" : classes,
					"assignments" : assignments
				}
			), 200, headers)
		
