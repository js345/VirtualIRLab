from flask import make_response, jsonify, current_app, request, render_template, session
from flask_restful import Resource, reqparse

from schema.User import User
from schema.DataSet import DataSet
from schema.Class import Class
from schema.Assignment import Assignment

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
		datasets = []

		for ds in DataSet.objects(author=user.name):
			datasets.append({"id":ds.id, "name":ds.name})

		# get all classes
		classes = []
		for class_ in Class.objects(instructor=user.name):
			classes.append(class_.name)

		# get all assignments
		assignments = []

		assignment_names = Assignment.objects.aggregate({
		    '$group': { '_id': '$name'}
		})

		assignment_names = list(assignment_names)

		# get all incomplete assignments
		incomplete_numbers = []
		for assignment_name in assignment_names:
			assignment_name = assignment_name['_id']
			incomplete_number = Assignment.objects(name=assignment_name,status=False).count()
			assignments.append({'name':assignment_name,'incomplete_number':incomplete_number})

		

		return make_response(render_template(
			"instructor.html", 
			data={
					"user" : json.dumps(user.to_json()),
					"datasets" : datasets,
					"classes" : classes,
					"assignments" : assignments
				}
			), 200, headers)
		
