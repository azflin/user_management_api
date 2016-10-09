from flask import request, jsonify
from flask.ext.restful import Resource, fields, marshal_with, abort

from models import User, Group, db


user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}
group_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.String
}


class UserResource(Resource):
    """
    /users/<int:id>
    GET: Return details of single user
    DELETE: Delete user
    PUT: Edit existing user. JSON payload must contain 'name' and/or 'email' key(s).
    """
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
            abort(400, message="Must use JSON.")
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
    """
    /users/
    GET: Return list of users
    POST: Create a user. JSON payload must contain 'name' and 'email' keys.
    """
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


class GroupResource(Resource):
    """
    /groups/<int:id>
    GET: Return details of single group
    DELETE: Delete a group
    PUT: Edit existing group. JSON payload must contain 'name'
    """
    @marshal_with(group_fields)
    def get(self, id):
        group = Group.query.get(id)
        if not group:
            abort(404, message="Group {} doesn't exist.".format(id))
        return group

    def delete(self, id):
        group = Group.query.get(id)
        if not group:
            abort(404, message="Group {} doesn't exist.".format(id))
        db.session.delete(group)
        db.session.commit()
        return {}, 204

    @marshal_with(group_fields)
    def put(self, id):
        group = Group.query.get(id)
        if not group:
            abort(404, message="Cannot edit group {} as it doesn't exist.".format(id))
        payload = request.get_json()
        if not payload:
            abort(400, message="Must use JSON.")
        if 'name' not in payload:
            abort(400, message="Bad validation - must have name.")
        group.name = payload['name']
        db.session.add(group)
        db.session.commit()
        return group, 201


class GroupListResource(Resource):
    """
    /groups/
    GET: Return list of groups
    POST: Create a group. JSON payload must contain 'name' key
    """
    @marshal_with(group_fields)
    def get(self):
        groups = Group.query.all()
        return groups

    @marshal_with(group_fields)
    def post(self):
        payload = request.get_json()
        if not payload:
            abort(400, message="Must use JSON.")
        if 'name' in payload:
            new_group = Group(name=payload['name'])
            db.session.add(new_group)
            db.session.commit()
            return new_group, 201
        else:
            abort(400, message="Bad validation - missing name.")


class UserGroupsResource(Resource):
    """
    /users/<int:id>/groups
    GET: Return groups of a single user
    """
    @marshal_with(group_fields)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user.groups


class GroupUsersResource(Resource):
    """
    /groups/<int:id>/users
    GET: Return users of a single group
    POST: Add or remove an existing user from group.
        Add: Use JSON payload of {"add": <user_id>}
        Remove: Use JSON payload of {"remove": <user_id>}
    """
    @marshal_with(user_fields)
    def get(self, id):
        group = Group.query.get(id)
        if not group:
            abort(404, message="Group {} doesn't exist.".format(id))
        return group.users.all()

    def post(self, id):
        group = Group.query.get(id)
        if not group:
            abort(404, message="Group {} doesn't exist.".format(id))
        payload = request.get_json()
        if not payload:
            abort(400, message="Must use JSON.")
        if 'add' not in payload and 'remove' not in payload:
            abort(400, message="Bad validation - payload must contain 'add' or 'remove' key.")
        if 'add' in payload:
            user = User.query.get(payload['add'])
            if not user:
                abort(404, message="User {} doesn't exist.".format(payload['add']))
            group.users.append(user)
            db.session.commit()
            return jsonify(message="User {} added to group {}.".format(payload['add'], id))
        elif 'remove' in payload:
            user = User.query.get(payload['remove'])
            if not user:
                abort(404, message="User {} doesn't exist.".format(payload['remove']))
            user_in_group = group.users.filter_by(id=payload['remove']).first()
            if not user_in_group:
                abort(400, message="User {} is not in group {}.".format(payload['remove'], id))
            group.users.remove(user_in_group)
            db.session.commit()
            return jsonify(message="User {} removed from group {}.".format(payload['remove'], id))