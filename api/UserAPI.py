from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api, reqparse
from flask_restful.utils import cors
from flaskext.mysql import MySQL

userParser = reqparse.RequestParser()
userParser.add_argument('name', type=str)
userParser.add_argument('group', type=str)
userParser.add_argument('passWord', type=str)
mysql = MySQL()
mysql.init_app(app)

class UserAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        name = args['name']
        passWord = args['passWord']
        group = args['group']
        if name is None or password is None or group is None:
            abort(400)

        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("INSERT INTO user VALUES("+ name + "," + group  + ","+ passWord + ")" )

        return ({'status': 'success'}, 201)
