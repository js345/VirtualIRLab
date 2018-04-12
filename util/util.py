from flask import current_app
from flask_login import current_user


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'toml', 'dat'}


def check_role(role):
    if not current_user.is_authenticated or current_user.role != role:
        return current_app.login_manager.unauthorized()
        # return redirect(url_for(current_user.role + 'api'))
