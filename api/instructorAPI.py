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
        if args['_method'] != 'DELETE':
            queries = [q for q in args['query[]'] if q != '']
            if not queries:
                flash('Empty Query!')
                return redirect(url_for('instructorapi'))

            ranker = args['ranker']
            assignment_name = args['assignment_name']
            dataset_name = args['ds_name']
            params = self.generate_params_dict(ranker, args['param[]'])
            instructor = User.objects(email=current_user.email).first()

            flash('Assignment Created!')
            return redirect(url_for('instructorapi'))
        else:
            pass

    @staticmethod
    def generate_queries(queries):
        result = []
        for q in queries:
            try:
                query = Query(q)
                query.save()
                result.append(query)
            finally:
                pass
        return result

    @staticmethod
    def generate_params_dict(ranker, params):
        rankers = {'OkapiBM25': ['k1', 'b', 'k3'],
                   'JelinekMercer': ['lambda'],
                   'DirichletPrior': ['mu'],
                   'AbsoluteDiscount': ['delta'],
                   'PivotedLength': ['s']}

        keys = rankers[ranker]
        result = {}
        for i in range(len(keys)):
            result[keys[i]] = params[i]
        return result
