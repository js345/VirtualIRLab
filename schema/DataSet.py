from schema import db


class DataSet(db.DynamicDocument):
    ds_name = db.StringField(required=True)
    author = db.ReferenceField("User",required=True)
    privacy = db.StringField(required=True)
    collaborators = db.ListField(db.ReferenceField('User'))