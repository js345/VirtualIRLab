from flask import make_response, render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from flask_restful import Resource, reqparse

from schema.DataSet import DataSet
from schema.User import User
from schema.Query import Query
from schema.Assignment import Assignment
from schema.Document import Document
from schema.Score import Score
from schema.Annotation import Annotation
from util.util import check_role
from mongoengine.errors import NotUniqueError, ValidationError

import os
from search.searcher import Searcher

parser = reqparse.RequestParser()
parser.add_argument('ds_name', type=str)
parser.add_argument('assignment_name', type=str)
parser.add_argument('query[]', type=str, action='append')
parser.add_argument('ranker', type=str)
parser.add_argument('param[]', type=str, action='append')
parser.add_argument('num_results', type=int)


class InstructorAPI(Resource):
    @login_required
    def get(self):
        check_role('instructor')
        datasets = [(d.name, d.author.name) for d in DataSet.objects()]
        instructor = User.objects(email=current_user.email).first()

        # TODO: Parse data to more structured format
        # per assignment, per query, sort doc, per doc, score and judgment count

        scores = []
        annotations = []
        assignments = []
        for a in Assignment.objects(instructor=instructor):
            assignments.append((a.name, a.data_set, a.ranker, a.params, a.num_results))
            for s in Score.objects(assignment=a):
                scores.append((s.result, s.query.content, s.document.path, s.document.name))
            for n in Annotation.objects(assignment=a):
                annotations.append(n)

        return make_response(render_template('instructor.html',
                                             datasets=datasets, assignments=assignments, scores=scores))

    @login_required
    def post(self):
        check_role('instructor')
        args = parser.parse_args()
        queries = [q for q in args['query[]'] if q != '']
        if not queries:
            flash('Empty Query!')
            return redirect(url_for('instructorapi'))

        ranker = args['ranker']
        assignment_name = args['assignment_name']
        dataset_name = args['ds_name']
        params = self.generate_params_dict(ranker, args['param[]'])
        num_results = args['num_results']

        instructor = User.objects(email=current_user.email).first()
        dataset = DataSet.objects(name=dataset_name).first()

        assignment = Assignment(name=assignment_name, instructor=instructor, data_set=dataset,
                                ranker=ranker, params=params, num_results=num_results)
        try:
            assignment.save()
        except (NotUniqueError, ValidationError):
            flash('Invalid Input!')
            return redirect(url_for('instructorapi'))

        q = self.generate_queries(queries)
        assignment.update(queries=q)

        try:
            self.search(assignment, dataset_name, queries, ranker, params, num_results)
        except Exception as e:
            print(e)

        flash('Assignment Created!')
        return redirect(url_for('instructorapi'))

    @staticmethod
    def search(assignment, dataset_name, queries, ranker, params, num_results):
        author = User.objects(email=current_user.email).first()
        path = os.path.join(current_app.root_path, 'data', author.name)
        searcher = Searcher(dataset_name, path)
        for query in queries:
            result = searcher.search(query, ranker, params, num_results)
            doc_path = result['path']
            doc_score = result['score']
            document = Document.objects(path=doc_path).first()
            q = Query(content=query)
            Score(result=doc_score, assignment=assignment, query=q, document=document).save()

    @staticmethod
    def generate_queries(queries):
        result = []
        for q in queries:
            query = Query.objects(content=q).first()
            if not query:
                query = Query(q)
                query.save()
            result.append(query)
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
