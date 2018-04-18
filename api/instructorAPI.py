from flask import make_response, render_template
from flask_login import login_required
from flask_restful import Resource, reqparse

from schema.DataSet import DataSet
from util.util import check_role

parser = reqparse.RequestParser()
parser.add_argument('assignment-name', type=str)
parser.add_argument('query[]', type=str, action='append')
parser.add_argument('ranker', type=str)
parser.add_argument('param[]', type=str, action='append')
parser.add_argument('_method', type=str)


class InstructorAPI(Resource):
    @login_required
    def get(self):
        check_role('instructor')

        datasets = [(d.name, d.author.name) for d in DataSet.objects()]

        assignments = []
        return make_response(render_template('instructor.html', datasets=datasets, assignments=assignments))

    @login_required
    def post(self):
        check_role('instructor')
        args = parser.parse_args()
        print(args)
