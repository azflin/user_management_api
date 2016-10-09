from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../user_management.db'
# Prevent flask_restful from adding annoying extra message to 404 responses
app.config['ERROR_404_HELP'] = False
db = SQLAlchemy(app)
api = Api(app)

from resources import UserResource, UserListResource

api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UserListResource, '/users/')
