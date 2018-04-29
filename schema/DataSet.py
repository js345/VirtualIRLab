from schema import db


class DataSet(db.Document):
    author = db.ReferenceField('User', required=True)
    name = db.StringField(required=True, unique_with=['author'])
