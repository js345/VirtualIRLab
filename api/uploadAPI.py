from flask import make_response, jsonify, current_app, request
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from util.utils import allowed_file
from util.exception import InvalidUsage

import os

parser = reqparse.RequestParser()
parser.add_argument('author', type=str)
parser.add_argument('ds_name', type=str)


class UploadAPI(Resource):
	"""
	API class for data uploading and viewing
	"""

	def post(self):
		"""
		Handle post request of data set uplpoading 
		using multipart/form data
		"""
		args = parser.parse_args()
		author = args['author']
		ds_name = args['ds_name']
		path = current_app.root_path + "/data/" + author + "/" + ds_name + "/"
		# To do: check validity of input
		if os.path.isdir(path):
			raise InvalidUsage("Dataset already exists", 400)
		os.mkdir(path)
		uploaded_files = request.files.getlist("file")
		# save the uploaded files and store in response
		response = {'files': []}
		for file in uploaded_files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(path, filename))
				response['files'].append(filename)
		return make_response(jsonify(response), 200)
