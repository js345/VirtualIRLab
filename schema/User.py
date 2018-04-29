from schema import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Document):
    meta = {'collection': 'test-user'}
    name = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    role = db.StringField(required=True, choices=('annotator', 'instructor'))
    password = db.StringField(required=True)
    credibility_score = db.FloatField(default=0.75)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)
