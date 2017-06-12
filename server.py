from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from schema import db, redis_store
from api.indexAPI import IndexAPI
from api.searchAPI import SearchAPI
from api.annotationAPI import AnnotationAPI
from api.uploadAPI import UploadAPI
from api.userAPI import UserAPI, LoginAPI
from api.assignmentAPI import AssignAPI, AssignmentAPI, AssignmentUpdateAPI
from api.instructorAPI import InstructorAPI
from api.annotatorAPI import AnnotatorAPI
from api.classAPI import ClassAPI
from api.logoutAPI import LogoutAPI

from util.exception import InvalidUsage

from flask import render_template

app = Flask(__name__, static_folder='static/', static_url_path='')
app.config.from_object('config')
api = Api(app)
CORS(app)

db.init_app(app)
redis_store.init_app(app)

api.add_resource(IndexAPI, '/index')
api.add_resource(SearchAPI, '/search/<string:author>/<string:ds_name>')
api.add_resource(AnnotationAPI, '/annotation')
api.add_resource(UploadAPI, '/upload')

api.add_resource(UserAPI, '/register')
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')

api.add_resource(AssignAPI, '/assign')
api.add_resource(AssignmentAPI, '/assignment/<string:instructor_name>/<string:assignment_name>')
api.add_resource(AssignmentUpdateAPI, '/assignment_update')

api.add_resource(InstructorAPI, '/instructor')
api.add_resource(AnnotatorAPI, '/annotator')
api.add_resource(ClassAPI, '/class')


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route("/student")
def student_page():
	return render_template("student.html")


if __name__ == '__main__':
	app.run(host='127.0.0.1')
