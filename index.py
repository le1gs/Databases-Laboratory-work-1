import sqlite3
from flask import Flask, json
from flask import request, Response
from flask_restful import Api,Resource
from flask.logging import default_handler

__author__ = ("le1gs","Misha Rumarchuk")

connect = sqlite3.connect("database.db", check_same_thread=False)
cursor = connect.cursor()

app = Flask(__name__)
api = Api()
class GetUsers(Resource):
	def get(self):
		cursor.execute(f"""SELECT * FROM users;""")
		return {'status':1,'users':cursor.fetchall()},200
class GetMessages(Resource):
	def get(self):
		cursor.execute(f"""SELECT u.user_name, m.message_text FROM users AS u INNER JOIN messages AS m ON u.user_id = m.user_id;""")
		return {'status':1,'messages':cursor.fetchall()},200
if __name__ == "__main__":
	cursor.execute("""CREATE TABLE IF NOT EXISTS users (
				user_id bigserial PRIMARY KEY NOT NULL,
				user_name VARCHAR (30) NOT NULL

	);""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
				message_id bigserial PRIMARY KEY NOT NULL,
				message_text VARCHAR (200) NOT NULL,
				user_id bigserial NOT NULL

	);""")
	api.add_resource(GetUsers,"/api/v1/users")
	api.add_resource(GetMessages,"/api/v1/messages")
	api.init_app(app)
	app.run(debug=True,port=8888,host="localhost")