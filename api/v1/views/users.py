#!/usr/bin/python3
'''
    Blueprint app_views decorators
    for HTTP requests that allow users
    to manipulate data in storage
'''

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import classes, storage
from models.user import User
import json


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_all_users():
    ''' Gets a dictionary of all users then jsonifies and returns it '''
    users = []
    all_users = storage.all("User")
    for key, val in all_users.items():
        users.append(val.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_one_user(user_id=None):
    ''' Gets a dictionary of specified user then jsonifies and returns it '''
    retrieved_user = storage.get("User", user_id)
    if retrieved_user == None:
        abort(404)
    else:
        return jsonify(retrieved_user.to_dict())


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_new_user():
    ''' Submits POST request to add a new user to the dictionary of users '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    else:
        if 'email' not in data:
            abort(400, 'Missing email')
        elif 'password' not in data:
            abort(400, 'Missing password')
        else:
            new_user = User()
            setattr(new_user, 'email', data['email'])
            setattr(new_user, 'password', data['password'])
            new_user.save()
            return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id=None):
    ''' Deletes a user from the dictionary of users '''
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        return jsonify({}), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def put_to_user(user_id=None):
    ''' Updates an item in the dictionary of users '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    else:
        for key, val in data.items():
            if key in obj.to_dict() and key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(obj, key, val)
        obj.save()
        return jsonify(obj.to_dict()), 200




