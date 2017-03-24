from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from schema import db
# from api.UserAPI import UserAPI
from api.searchAPI import SearchAPI

app = Flask(__name__, static_folder='static/', static_url_path='')
app.config.from_object('config')
api = Api(app)
CORS(app)

db.init_app(app)

# api.add_resource(UserAPI, '/register')
api.add_resource(SearchAPI, '/search/<string:ds_name>')

if __name__ == '__main__':
    app.run(host='127.0.0.1')
