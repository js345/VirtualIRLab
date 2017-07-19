from flask import make_response, render_template, current_app, jsonify, request, session
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()

class AlertAPI(Resource):
	def get(self, url, message):
		headers = {'Content-Type': 'text/html'}

		print(message)
		print(url)
		return make_response(
			render_template('notification.html', 
				data={"url": "/" + url, "message":message})
			,200,headers)