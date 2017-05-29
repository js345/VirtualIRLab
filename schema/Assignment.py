from schema import db

class Assignment(db.DynamicDocument):
    instructor = db.ReferenceField('User', required=True)
    annotator = db.ReferenceField('User')
    dataset = db.ReferenceField('DataSet', required=True)
    query = db.StringField(required=True)
    status = db.BooleanField(required=True)
    view_status = db.BooleanField(required=True)
    ranker = db.StringField(required=True)
    params = db.StringField(required=True)
