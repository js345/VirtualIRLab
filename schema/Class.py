from schema import db

class Class(db.Document):
    instructor = db.StringField(required=True)
    name = db.StringField(required=True)
    password = db.StringField(required=True)