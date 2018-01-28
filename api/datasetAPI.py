from flask import make_response, render_template, current_app, jsonify, session
from flask_restful import Resource, reqparse
from util.userAuth import annotator_auth_required

from schema.DataSet import DataSet

from schema.User import User
from schema.Query import Query
from schema.Assignment import Assignment

import os

parser = reqparse.RequestParser()



class DatasetAPI(Resource):
    def post(self):
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


parser.add_argument('ds_id', type=str)
parser.add_argument('ds_name', type=str)
parser.add_argument('ds_privacy', type=str)
parser.add_argument('collaborators', type=str, action='append')

class DatasetUpdateAPI(Resource):
    def post(self):
        headers = {'Content-Type': 'application/json'}

        args = parser.parse_args()
        ds_id = args['ds_id']
        ds_name = args['ds_name']
        ds_privacy = args['ds_privacy']
        collaborators = args['collaborators']

        ds = DataSet.objects(id=ds_id).first()

        # change ds name in disk
        user_id = session['user_id'];
        user = User.objects(id=user_id).first()

        if ds_name != "":
            old_ds_path = current_app.root_path + "/data/" + user.name + "/" + ds.ds_name
            new_ds_path = current_app.root_path + "/data/" + user.name + "/" + ds_name
            os.rename(old_ds_path, new_ds_path)
            ds.ds_name = ds_name

        if ds_privacy != "":
            ds.privacy = ds_privacy

        if ds.privacy == 'public':
            ds.save()
            return make_response(jsonify({'message':"This dataset is already public."}), 200, headers)

        if collaborators is not None:
            for collaborator in collaborators:
                if User.objects(name=collaborator).first() == None:
                    return make_response(jsonify({'message':"Collaborator(s) don't exist"}), 200, headers)

                ds.collaborators.append(User.objects(name=collaborator).first())
        ds.save()

        return make_response(jsonify({'message':"OK"}), 200, headers)








        