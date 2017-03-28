from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_redis import FlaskRedis

db = MongoEngine()
bcrypt = Bcrypt()
redis_store = FlaskRedis()
