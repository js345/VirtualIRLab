from flask import make_response, jsonify, current_app, request, render_template
from flask_restful import Resource, reqparse

from util.exception import InvalidUsage


class InstructorAPI(Resource):

	def get(self):
		"""
		Render Instructor UI
		"""
		headers = {'Content-Type': 'text/html'}
		return make_response(render_template('instructor.html'), 200, headers)
