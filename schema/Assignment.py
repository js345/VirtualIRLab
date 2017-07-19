from schema import db

class Assignment(db.DynamicDocument):
    name = db.StringField(required=True)
    instructor = db.ReferenceField('User', required=True)
    annotator = db.ReferenceField('User', required=True)
    dataset = db.ReferenceField('DataSet')
    query = db.StringField(required=True)
    status = db.BooleanField(required=True)
    view_status = db.BooleanField(required=True)
    ranker = db.StringField(required=True)
    params = db.DictField(required=True)
    doc_scores = db.DictField(required=True)
    deadline = db.StringField(required=True)
