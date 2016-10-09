from flask import request
from flask.ext.restful import Resource, fields, marshal_with, abort

from models import User, Group, db


user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="User {} doesn't exist.".format(id))
        return user

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="User {} doesn't exist.".format(id))
        db.session.delete(user)
        db.session.commit()
        return {}, 204

    @marshal_with(user_fields)
    def put(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="Cannot edit user {} as it doesn't exist.".format(id))
        payload = request.get_json()
        if not payload:
            abort(400, message="Must use JSON")
        if 'name' not in payload and 'email' not in payload:
            abort(400, message="Bad validation - payload must have email and/or name.")
        if 'name' in payload:
            user.name = payload['name']
        if 'email' in payload:
            user.email = payload['email']
        db.session.add(user)
        db.session.commit()
        return user, 201


class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        payload = request.get_json()
        if not payload:
            abort(400, message="Must use JSON.")
        if 'name' in payload and 'email' in payload:
            new_user = User(name=payload['name'], email=payload['email'])
            db.session.add(new_user)
            db.session.commit()
            return new_user, 201
        else:
            abort(400, message="Bad validation - missing at least one of name or email.")