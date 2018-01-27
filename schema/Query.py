from schema import db


class Query(db.DynamicDocument):
    content = db.StringField(required=True)
    assignment = db.ReferenceField('Assignment', required=True)
    doc_scores = db.DictField(required=True)
    creator = db.ReferenceField('User', required=True)
