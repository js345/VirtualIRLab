from flask import redirect, make_response, render_template, session
from flask_restful import Resource, reqparse
from schema.User import User
from util.userAuth import login_auth_required


class IndexAPI(Resource):
	@login_auth_required
	def get(self):
		headers = {'Content-Type': 'text/html'}

		# nav user to right page
		user_id = session['user_id']
		user = User.objects(id=user_id).first()

		if user.group == "instructor":
			return redirect("/instructor")
		elif user.group == "annotator":
			return redirect("/annotator")

		return render_template("index.html")