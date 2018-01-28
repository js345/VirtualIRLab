from schema import db


class Document(db.DynamicDocument):
	name = db.StringField(require=True)
	dataset = db.ReferenceField("DataSet", require=True)