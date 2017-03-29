from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from schema import db, redis_store
# from api.UserAPI import UserAPI
from api.searchAPI import SearchAPI
from api.annotationAPI import AnnotationAPI

app = Flask(__name__, static_folder='static/', static_url_path='')
app.config.from_object('config')
api = Api(app)
CORS(app)

db.init_app(app)
redis_store.init_app(app)
redis_store.set('foo', 'bar2')

# api.add_resource(UserAPI, '/register')
api.add_resource(SearchAPI, '/search/<string:author>/<string:ds_name>')
api.add_resource(AnnotationAPI, '/annotation')

if __name__ == '__main__':
    app.run(host='127.0.0.1')
