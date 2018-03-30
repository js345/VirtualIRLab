from schema import db


class Annotation(db.DynamicDocument):
    annotator = db.ReferenceField('User', required=True)
    data_set = db.ReferenceField('DataSet', required=True)
    query = db.ReferenceField('Query', required=True)
    doc = db.ReferenceField('Document', required=True)
    judgement = db.BooleanField(required=True)
    assignment = db.ReferenceField('Assignment', default=None)
