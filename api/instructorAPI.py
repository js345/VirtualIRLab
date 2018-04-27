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

        assignments = {}
        for assignment in Assignment.objects(instructor=instructor):
            assignments[(assignment.name, assignment.instructor.name)] = (self.get_judgement_score(assignment))

        result = {('a1', 'i1'): {'q1': {'d1': {'score': 1, 'relevant': 2, 'irrelevant': 3},
                                        'd2': {'score': 4, 'relevant': 5, 'irrelevant': 6}},
                                 'q2': {'d1': {'score': 11, 'relevant': 22, 'irrelevant': 33},
                                        'd2': {'score': 44, 'relevant': 55, 'irrelevant': 66}}},

                  ('a2', 'i2'): {'q1': {'d1': {'score': 1111, 'relevant': 2, 'irrelevant': 3},
                                        'd2': {'score': 4, 'relevant': 5555, 'irrelevant': 6}}},
                  }

        return make_response(render_template('instructor.html',
                                             datasets=datasets, assignments=result))

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
            results = searcher.search(query, ranker, params, num_results)['results']
            for result in results:
                doc_path = str(os.path.join(path, result['path'].encode('utf8')[2:]))
                doc_score = result['score']
                document = Document.objects(path=doc_path).first()
                q = Query.objects(content=query).first()
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
            result[keys[i]] = float(params[i])
        return result

    @staticmethod
    def get_judgement_score(assignment):
        queries = assignment.queries
        scores = Score.objects(assignment=assignment)
        result = {}
        for query in queries:
            query_result = {}
            for doc_score in scores.filter(query=query):
                score = doc_score.result
                doc = doc_score.document
                relevant = Annotation.objects(doc=doc, query=query, assignment=assignment, judgement=True).count()
                irrelevant = Annotation.objects(doc=doc, query=query, assignment=assignment, judgement=False).count()
                doc_result = {'score': score, 'relevant': relevant, 'irrelevant': irrelevant}
                query_result[doc.name] = doc_result
            result[query.content] = query_result
        return result
