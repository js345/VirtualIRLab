from flask import make_response, jsonify, current_app, request, render_template, session
from flask_restful import Resource, reqparse
from schema.User import User
from schema import redis_store
from util.userAuth import auth_required
from util.exception import InvalidUsage
import os,json

class InstructorAPI(Resource):

	@auth_required
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
		path = current_app.root_path + "/data/" + user.name
		datasets = []

		for directory in os.listdir(path):
			datasets.append(directory)

		return make_response(render_template(
			"instructor.html", 
			data={
					"user" : json.dumps(user.to_json()),
					"datasets" : datasets
				}
			), 200, headers)
		
