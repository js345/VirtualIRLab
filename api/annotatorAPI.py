from flask import make_response, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from flask_restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError

from schema.Annotation import Annotation
from schema.Assignment import Assignment
from schema.DataSet import DataSet
from schema.Document import Document
from schema.Query import Query
from schema.User import User
from util.util import check_role, parse_multi_form


class AnnotatorAPI(Resource):
    @login_required
    def get(self):
        check_role('annotator')
        return make_response(
            render_template('annotator.html', datasets=DataSet.objects(), assignments=Assignment.objects()))

    @login_required
    def post(self):
        check_role('annotator')
        args = self.parse_args()
        msg = 'Invalid Submission!'
        if self.store_annotations(args['annotation'], args['assignment_id']):
            msg = 'Assignment Submitted!'
        flash(msg)
        return redirect(url_for('annotatorapi'))

    @staticmethod
    def store_annotations(annotations, assignment_id):
        assignment = Assignment.objects(id=assignment_id).first()
        for query_id in annotations:
            query = Query.objects(id=query_id).first()
            for doc_id in annotations[query_id]:
                result = annotations[query_id][doc_id]
                judgement = False
                if result == 'T':
                    judgement = True
                doc = Document.objects(id=doc_id).first()
                user = User.objects(email=current_user.email).first()
                try:
                    Annotation(user, query, doc, judgement, assignment).save()
                except (NotUniqueError, ValidationError):
                    return False
        return True

    @staticmethod
    def parse_args():
        parser = reqparse.RequestParser()
        parser.add_argument('assignment_id', type=str)
        args = parser.parse_args()
        args['annotation'] = parse_multi_form(request.form)['annotation']
        return args
