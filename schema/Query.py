from schema import db


class Query(db.DynamicDocument):
    content = db.StringField(required=True)
    data_set = db.ReferenceField('DataSet', required=True)
    creator = db.ReferenceField('User', required=True)
