from flask import make_response, render_template, current_app, jsonify, flash, redirect, url_for
from flask_restful import Resource, reqparse
from flask_login import login_required, current_user

from schema.DataSet import DataSet

from schema.User import User
from schema.Query import Query
from schema.Assignment import Assignment
from schema.Score import Score
from mongoengine.queryset.visitor import Q
from util.util import check_role, parse_multi_form

parser = reqparse.RequestParser()
parser.add_argument('instructor', type=str)
parser.add_argument('annotator', type=str)
parser.add_argument('dataset', type=str)
parser.add_argument('query', type=str)
parser.add_argument('ranker', type=str)
parser.add_argument('params', type=dict)
parser.add_argument('status', type=bool)
parser.add_argument('content', type=str)
parser.add_argument('creator', type=str)


class AssignmentAPI(Resource):
    @login_required
    def get(self, instructor_name, assignment_name):
        # TODO: annotation view
        check_role('annotator')
        instructor = User.objects(name=instructor_name).first()
        assignment = Assignment.objects(Q(name=assignment_name) & Q(instructor=instructor)).first()
        if not assignment:
            flash('No Such Assignment!')
            return redirect(url_for('annotatorapi'))
        queries = {}
        for q in assignment.queries:
            docs = Score.objects(Q(query=q) & Q(assignment=assignment))
            queries[q.content] = [doc.document for doc in docs]

        test = {'testQ1': ['d1', 'd2'], 'testQ2': ['d1', 'd2']}

        return make_response(render_template('assignment.html', assignment=assignment, queries=test))
