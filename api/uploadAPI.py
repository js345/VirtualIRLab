from flask import make_response, jsonify, current_app, request, render_template, session
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from util.utils import allowed_file
from util.exception import InvalidUsage

from schema import db
from schema.DataSet import DataSet
from schema.User import User

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
		user_id = session['user_id']
		user = User.objects(id=user_id).first()
		print(user.name)
		return make_response(render_template('upload_file.html', author=user), 200, headers)

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
		# if os.path.isdir(path):
		# 	raise InvalidUsage("Dataset already exists", 400)
		# os.mkdir(path)

		# save new ds object

		# ds = DataSet()
		# ds.name = ds_name
		# ds.author = User.objects(name=author_name).first()
		# ds.save()

		uploaded_files = request.files.getlist("file")
		# save the uploaded files to disk
		response = {'files': []}
		for file in uploaded_files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(path, filename))
				response['files'].append(filename)

		# create config files
		if len(os.listdir(path)) != 0:
			file_corpus = open(path+"/dataset-full-corpus.txt", "w")
			file_toml = open(path+"/file.toml", "w")
			file_metadata = open(path+"/metadata.data", "w")

			for file in os.listdir(path):
				if file[-3:] == "txt" and file != "dataset-full-corpus.txt":
					file_corpus.write("[None] " + file + "\n")
					file_metadata.write(file + " " + file[:-4] + "\n")

			file_toml.write("type = \"file-corpus\"" + "\n")
			file_toml.write("list = \"dataset\"")

			file_corpus.close()
			file_toml.close()
			file_metadata.close()

		return make_response(jsonify(response), 200)
