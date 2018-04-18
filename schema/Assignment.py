from schema import db


class Assignment(db.DynamicDocument):
    instructor = db.ReferenceField('User', required=True)
    annotators = db.ListField(db.ReferenceField('User'), default=[])
    data_set = db.ReferenceField('DataSet', required=True)
    queries = db.ListField(db.ReferenceField('Query'), default=[])
    ranker = db.StringField(required=True)
    params = db.DictField(required=True)
