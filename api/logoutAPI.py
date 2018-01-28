from flask import redirect, make_response, render_template, session
from flask_restful import Resource, reqparse
from schema import redis_store
from util.userAuth import login_auth_required

class LogoutAPI(Resource):
	@login_auth_required
	def get(self):
		headers = {'Content-Type': 'text/html'}

		session["token"] = None
		session["user_id"] = None

		return redirect("/index")