from schema import db


class Document(db.DynamicDocument):
    name = db.StringField(required=True)
    data_set = db.ReferenceField('DataSet', required=True)
    path = db.StringField(required=True, unique=True)
