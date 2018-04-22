from flask import current_app
from flask_login import current_user


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'toml', 'dat'}


def check_role(role):
    if not current_user.is_authenticated or current_user.role != role:
        return current_app.login_manager.unauthorized()
        # return redirect(url_for(current_user.role + 'api'))


def parse_multi_form(form):
    data = {}
    for url_k in form:
        v = form[url_k]
        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i + 1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v
    return data
