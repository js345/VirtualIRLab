from schema import db


class Annotation(db.DynamicDocument):
    annotator = db.ReferenceField('User', required=True)
    document = db.ReferenceField("Document", required=True)
    assignment = db.ReferenceField("Assignment", required=True)
    judgement = db.StringField(required=True)
