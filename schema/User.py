from schema import db


class User(db.DynamicDocument):
    name = db.StringField(required=True)
    group = db.IntField(required=True)
    password = db.StringField(required=True)
