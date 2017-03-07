from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api
from flask_restful.utils import cors
from flaskext.mysql import MySQL


app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
api.decorators = [cors.crossdomain(origin='*', headers='my-header, accept, content-type, token')]

mysql = MySQL()
mysql.init_app(app)
#conn = mysql.connect()

if __name__ == '__main__':
    app.run(host='127.0.0.1')
