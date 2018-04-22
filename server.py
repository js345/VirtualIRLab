from flask import Flask, jsonify, redirect, url_for
from flask import render_template
from flask_cors import CORS
from flask_restful import Api
from flask_login import LoginManager, current_user, login_required
from api.assignmentAPI import AssignmentAPI
from api.instructorAPI import InstructorAPI
from api.annotatorAPI import AnnotatorAPI
from api.searchAPI import SearchAPI
from api.datasetAPI import DatasetAPI
from api.userAPI import RegisterAPI, LoginAPI, LogoutAPI
from api.documentAPI import DocumentAPI
from schema import db, redis_store, User
from util.exception import InvalidUsage

app = Flask(__name__, static_folder='static/', static_url_path='')
app.config.from_object('config')
api = Api(app)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main'

db.init_app(app)

api.add_resource(RegisterAPI, '/register')
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')

api.add_resource(InstructorAPI, '/instructor')
api.add_resource(DatasetAPI, '/upload')
api.add_resource(AnnotatorAPI, '/annotator')
api.add_resource(AssignmentAPI, '/assignment/<string:instructor_name>/<string:assignment_name>')

api.add_resource(SearchAPI, '/search/<string:author>/<string:ds_name>')
api.add_resource(DocumentAPI, '/document/<string:doc_id>')

@login_manager.user_loader
def load_user(user_id):
    return User.User.objects(pk=user_id).first()


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def main():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1')


# searchAPI     - check dataset existence, query search

# annotatorAPI  - annotator post annotations
# instructorAPI - render assignment view
# assignmentAPI - render annotation assignment
