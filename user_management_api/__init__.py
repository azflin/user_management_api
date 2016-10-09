from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../user_management.db'
# Prevent flask_restful from adding annoying extra message to 404 responses
app.config['ERROR_404_HELP'] = False
db = SQLAlchemy(app)
api = Api(app)

from resources import UserResource, UserListResource, GroupResource, GroupListResource,\
    UserGroupsResource, GroupUsersResource

api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UserListResource, '/users/')
api.add_resource(GroupResource, '/groups/<int:id>')
api.add_resource(GroupListResource, '/groups/')
api.add_resource(UserGroupsResource, '/users/<int:id>/groups')
api.add_resource(GroupUsersResource, '/groups/<int:id>/users')