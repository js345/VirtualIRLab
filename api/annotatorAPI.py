from flask import make_response, render_template, current_app, jsonify, session
from flask_restful import Resource, reqparse
from util.userAuth import annotator_auth_required

from schema.DataSet import DataSet

from schema.User import User
from schema.Query import Query
from schema.Assignment import Assignment

parser = reqparse.RequestParser()



class AnnotatorAPI(Resource):

    @annotator_auth_required
    def get(self):
        headers = {'Content-Type': 'text/html'}

        # get user
        user_id = session['user_id'];
        user = User.objects(id=user_id).first()

        # get all assignments
        assignments = Assignment.objects(annotator=user)

        for assignment in assignments:
            assignment['author'] = assignment.instructor.name

        return make_response(
            render_template(
                "annotator.html",
                data={
                    "assignments" : assignments,
                    "user" : user
                }), 
            200, headers)


    def post(self):
        headers = {'Content-Type': 'application/json'}
        

        return make_response(render_template("annotator.html"), 200, headers)