from schema import db

class Assignment(db.DynamicDocument):
    name = db.StringField(required=True)
    instructor = db.ReferenceField('User', required=True)
    dataset = db.ReferenceField('DataSet')
    annotators = db.ListField(db.ReferenceField('User'),required=True)
    statuses = db.DictField(required=True)
    ranker = db.StringField(required=True)
    params = db.DictField(required=True)
    deadline = db.StringField(required=True)