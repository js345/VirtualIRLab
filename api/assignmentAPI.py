from flask import make_response, render_template, flash, redirect, url_for
from flask_login import login_required
from flask_restful import Resource

from schema.Assignment import Assignment
from schema.Annotation import Annotation
from schema.Score import Score
from schema.User import User
from util.util import check_role
from util.nsa import output
import numpy as np

class AssignmentAPI(Resource):
    @login_required
    def get(self, instructor_name, assignment_name):
        # TODO: annotation view
        check_role('annotator')
        instructor = User.objects(name=instructor_name).first()
        assignment = Assignment.objects(name=assignment_name, instructor=instructor).first()
        if not assignment:
            flash('No Such Assignment!')
            return redirect(url_for('annotatorapi'))
        queries = {}
        assignment_score = Score.objects(assignment=assignment)
        AssignmentAPI.query_nsa_filter(assignment)
        for q in assignment.queries_need_to_show:
            scores = assignment_score.filter(query=q)
            queries[q] = [score.document for score in scores]

        return make_response(render_template('assignment.html', assignment=assignment, queries=queries))

    @staticmethod
    def query_nsa_filter(assignment):
        queries_need_to_show_new = []
        for q in assignment.queries_need_to_show:
            annotations = Annotation.objects(query=q)
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
            res = output.Decision(students_annotations_res, credibility_scores)
            if not res.completed:
                queries_need_to_show_new.append(q)
                for i in range(len(student_list)):
                    userobj = User.objects(id=student_list[i]).first()
                    userobj.update(credibility_score=res.new_credibility_scores[i])
        assignment.update(queries_need_to_show=queries_need_to_show_new)
