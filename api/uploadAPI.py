from flask import make_response, jsonify, current_app, request, render_template, flash, redirect, url_for
from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from util.util import allowed_file
from util.exception import InvalidUsage
from util.util import check_role
import os

parser = reqparse.RequestParser()
parser.add_argument('ds_name', type=str)


class UploadAPI(Resource):
    @login_required
    def get(self):
        check_role('instructor')
        return make_response(render_template('upload.html'))

    @login_required
    def post(self):
        check_role('instructor')
        args = parser.parse_args()

        author = current_user.name
        ds_name = args['name']

        files = request.files.getlist('file')
        for f in files:
            print(f.filename)

        msg = "Dataset uploaded."
        flash(msg)
        return redirect(url_for('instructorapi'))

        # path = current_app.root_path + "/data/" + author + "/" + ds_name + "/"
        # # To do: check validity of input
        # if os.path.isdir(path):
        #     raise InvalidUsage("Dataset already exists", 400)
        # os.mkdir(path)
        # uploaded_files = request.files.getlist("file")
        # # # save the uploaded files and store in response
        # response = {'files': []}
        # for file in uploaded_files:
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         file.save(os.path.join(path, filename))
        #         response['files'].append(filename)
        # return make_response(jsonify(response), 200)
