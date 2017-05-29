from flask import make_response, jsonify, current_app, request, render_template
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from util.utils import allowed_file
from util.exception import InvalidUsage
from schema.DataSet import DataSet
import os

parser = reqparse.RequestParser()
parser.add_argument('author', type=str)
parser.add_argument('ds_name', type=str)


class UploadAPI(Resource):
	"""
	API class for data uploading and viewing
	"""

	def get(self):
		"""
		Render upload UI
		"""
		headers = {'Content-Type': 'text/html'}
		return make_response(render_template('upload_file.html'), 200, headers)

	def post(self):
		"""
		Handle post request of data set uplpoading 
		using multipart/form data
		"""
		args = parser.parse_args()
		author_name = args['author']
		ds_name = args['ds_name']

		# fisrt check author path
		author_path = current_app.root_path + "/data/" + author_name

		if not os.path.exists(author_path):
			os.mkdir(author_path)

		# create data set
		path = current_app.root_path + "/data/" + author_name + "/" + ds_name + "/"
		# To do: check validity of input
		if os.path.isdir(path):
			raise InvalidUsage("Dataset already exists", 400)
		os.mkdir(path)

		# save new ds object
		ds = DataSet()
		ds.ds_name = ds_name
		ds.author = author_name
		ds.save()

		uploaded_files = request.files.getlist("file")
		# save the uploaded files to disk
		response = {'files': []}
		for file in uploaded_files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(path, filename))
				response['files'].append(filename)

		return make_response(jsonify(response), 200)
