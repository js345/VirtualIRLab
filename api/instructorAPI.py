from flask import make_response, render_template
from flask_login import login_required
from flask_restful import Resource

from schema.DataSet import DataSet
from util.util import check_role


class InstructorAPI(Resource):
    @login_required
    def get(self):
        check_role('instructor')

        # datasets = [('a', '1'), ('b', '2')]
        datasets = [(d.name, d.author.name) for d in DataSet.objects()]

        assignments = []
        return make_response(render_template('instructor.html', datasets=datasets, assignments=assignments))
