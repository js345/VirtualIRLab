from schema import db


class Annotation(db.DynamicDocument):
    annotator = db.ReferenceField('User', required=True)
    document = db.ReferenceField("Document", required=True)
    query = db.ReferenceField('Query', required=True)
    judgement = db.StringField(required=True)
