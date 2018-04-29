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
from util.nsa import OutputDecision
import numpy as np

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
        AnnotatorAPI.query_nsa_filter(assignment)
        return True

    @staticmethod
    def parse_args():
        parser = reqparse.RequestParser()
        parser.add_argument('assignment_id', type=str)
        args = parser.parse_args()
        args['annotation'] = parse_multi_form(request.form)['annotation']
        return args

    @staticmethod
    def query_nsa_filter(assignment):
        queries_need_to_show_new = []
        for q in assignment.queries_need_to_show:
            all_annotations_of_the_query = Annotation.objects(query=q)
            annotations = []
            for annotation in all_annotations_of_the_query:
                if annotation.assignment.name == assignment.name and annotation.assignment.instructor == assignment.instructor:
                    annotations.append(annotation)
            students = {}
            student_list = []
            documents = {}
            for annotation in annotations:
                if annotation.annotator.id not in students.keys():
                    students[annotation.annotator.id] = len(students)
                    student_list.append(annotation.annotator.id)
                if annotation.doc.id not in documents.keys():
                    documents[annotation.doc.id] = len(documents)
            students_annotations_res = np.zeros((len(documents), len(students)), dtype=int)
            credibility_scores = np.zeros(len(students))
            for annotation in annotations:
                score = 1 if annotation.judgement else -1
                students_annotations_res[documents[annotation.doc.id]][students[annotation.annotator.id]] = score
            for studentID, pos in students.items():
                credibility_scores[pos] = User.objects(id=studentID).first().credibility_score
            res = OutputDecision.Decision(students_annotations_res, credibility_scores)
            if res.completed:
                for i in range(len(student_list)):
                    userobj = User.objects(id=student_list[i]).first()
                    old_credibility_score = userobj.credibility_score
                    new_credibility_score = old_credibility_score + (
                            res.new_credibility_scores[i] - old_credibility_score) / 3
                    userobj.update(credibility_score=new_credibility_score)
            else:
                queries_need_to_show_new.append(q)
        assignment.update(queries_need_to_show=queries_need_to_show_new)
