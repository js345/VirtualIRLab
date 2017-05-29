from schema import db

class Class(db.DynamicDocument):
    instructor = db.ReferenceField('User')
    name = db.StringField(required=True)
    password = db.StringField(required=True)