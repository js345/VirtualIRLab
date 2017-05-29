from schema import db

class Class(db.DynamicDocument):
    instructor = db.StringField(required=True)
    name = db.StringField(required=True)
    password = db.StringField(required=True)