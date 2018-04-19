from schema import db


class Score(db.DynamicDocument):
    result = db.FloatField(required=True)
    assignment = db.ReferenceField('Assignment', required=True)
    query = db.ReferenceField('Query', required=True)
    document = db.ReferenceField('Document', required=True)
