from schema import db


class DataSet(db.DynamicDocument):
    name = db.StringField(required=True)
    author = db.ReferenceField("User",required=True)
