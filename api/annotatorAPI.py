from flask import make_response, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from flask_restful import Resource, reqparse

from schema.DataSet import DataSet
from schema.User import User
from schema.Query import Query
from schema.Assignment import Assignment
from util.util import check_role

parser = reqparse.RequestParser()
parser.add_argument('assignment_name', type=str)
parser.add_argument('annotation[][]', type=dict)


class AnnotatorAPI(Resource):
    @login_required
    def get(self):
        check_role('annotator')
        return make_response(
            render_template('annotator.html', datasets=DataSet.objects(), assignments=Assignment.objects()))

    @login_required
    def post(self):
        check_role('annotator')

        a = self.parse_multi_form(request.form)
        print(a)
        print(request.form.getlist('annotation[][]'))
        # flash('Assignment Submitted!')
        # return make_response(render_template('annotator.html'))
