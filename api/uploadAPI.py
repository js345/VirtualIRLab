from flask import make_response, jsonify, current_app, request, render_template, flash, redirect, url_for
from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from util.util import allowed_file
from util.exception import InvalidUsage
from schema.DataSet import DataSet
from schema.User import User
from schema.Document import Document
from util.util import check_role, allowed_file
from mongoengine.errors import NotUniqueError
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
        # check file format
        files = request.files.getlist('file')
        for f in files:
            if not f or not allowed_file(f.filename):
                flash('Wrong file format.')
                return redirect(url_for('uploadapi'))
        # create dataset object
        args = parser.parse_args()
        author = User.objects(email=current_user.email).first()
        ds_name = args['ds_name']
        print(author.email, ds_name)
        dataset = DataSet(author, ds_name)
        try:
            dataset.save()
        except NotUniqueError:
            flash('Dataset name is occupied.')
            return redirect(url_for('uploadapi'))
        # save documents
        author_dir = os.path.join(current_app.root_path, 'data', author.name)
        if not os.path.exists(author_dir):
            os.mkdir(author_dir)
        ds_dir = os.path.join(author_dir, ds_name)
        os.mkdir(ds_dir)
        for f in files:
            filename = secure_filename(f.filename)
            f_path = os.path.join(ds_dir, filename)
            f.save(f_path)
            doc = Document(f.filename, dataset, f_path)
            doc.save()
        # create config files - copied from guoqiao's gift
        if len(os.listdir(ds_dir)) != 0:
            file_corpus = open(ds_dir + "/dataset-full-corpus.txt", "w")
            file_toml = open(ds_dir + "/file.toml", "w")
            file_metadata = open(ds_dir + "/metadata.data", "w")

            for file in os.listdir(ds_dir):
                if file[-3:] == "txt" and file != "dataset-full-corpus.txt":
                    file_corpus.write("[None] " + file + "\n")
                    file_metadata.write(file + " " + file[:-4] + "\n")

            file_toml.write("type = \"file-corpus\"" + "\n")
            file_toml.write("list = \"dataset\"")

            file_corpus.close()
            file_toml.close()
            file_metadata.close()

        flash('Dataset uploaded.')
        return redirect(url_for('instructorapi'))
