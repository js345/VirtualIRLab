from schema import db, bcrypt
from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer)


class User(db.DynamicDocument):
    name = db.StringField(required=True, unique=True)
    group = db.StringField(required=True)
    password_hash = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    assignment = db.ReferenceField("Assignment")
    class_ = db.ReferenceField("Class")

    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        s = Serializer(current_app.config.get('SECRET_KEY'),expires_in=99999)
        return s.dumps(str(self.id))