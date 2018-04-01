from flask import make_response, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_restful import Resource


class InstructorAPI(Resource):
    @login_required
    def get(self):
        if not current_user.is_authenticated or current_user.role != 'instructor':
            return redirect(url_for(current_user.role + 'api'))
        """
        Render Instructor UI
        """
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('instructor.html'), 200, headers)
