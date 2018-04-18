from flask import make_response, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_restful import Resource, reqparse

from schema.DataSet import DataSet
from schema.User import User
from schema.Query import Query
from util.util import check_role

parser = reqparse.RequestParser()
parser.add_argument('ds_name', type=str)
parser.add_argument('assignment_name', type=str)
parser.add_argument('query[]', type=str, action='append')
parser.add_argument('ranker', type=str)
parser.add_argument('param[]', type=str, action='append')
parser.add_argument('_method', type=str)


class AnnotatorAPI(Resource):
    @login_required
    def get(self):
        check_role('annotator')
        assignments = []
        return make_response(render_template('annotator.html', assignments=assignments))
