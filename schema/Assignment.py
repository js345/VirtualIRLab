from schema import db

class Assignment(db.DynamicDocument):
    instructor = db.ReferenceField('User')
    class_ = db.ReferenceField('Class', required=True)
    dataset = db.ReferenceField('DataSet', required=True)
    query = db.ReferenceField('Query', required=True)
    status = db.BooleanField(required=True)
    ranker = db.StringField(required=True)
    params = db.StringField(required=True)
