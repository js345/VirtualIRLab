from flask import redirect, make_response, render_template, session
from flask_restful import Resource, reqparse
from schema.User import User
from util.userAuth import login_auth_required


class IndexAPI(Resource):
	def get(self):
		headers = {'Content-Type': 'text/html'}

		return make_response(render_template("index.html"), 200, headers)