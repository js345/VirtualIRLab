from schema import db


class DataSet(db.DynamicDocument):
    ds_name = db.StringField(required=True)
    author = db.ReferenceField('User', required=True)
    path = db.StringField(required=True)
