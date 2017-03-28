from schema import db, bcrypt


class User(db.DynamicDocument):
    name = db.StringField(required=True, unique=True)
    group = db.IntField(required=True)
    password_hash = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)

    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
