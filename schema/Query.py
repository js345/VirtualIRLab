from schema import db


class Query(db.DynamicDocument):
    content = db.StringField(required=True, unique=True)
