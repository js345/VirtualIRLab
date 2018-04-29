from flask import make_response, render_template, flash, redirect, url_for
from flask_login import login_required
from flask_restful import Resource

from schema.Assignment import Assignment
from schema.Score import Score
from schema.User import User
from util.util import check_role


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
        for q in assignment.queries_need_to_show:
            scores = assignment_score.filter(query=q)
            queries[q] = [score.document for score in scores]

        return make_response(render_template('assignment.html', assignment=assignment, queries=queries))


