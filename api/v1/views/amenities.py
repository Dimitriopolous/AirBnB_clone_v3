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
from models.amenity import Amenity
import json


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_all_amenities():
    ''' Gets a dictionary of all amenities then jsonifies and returns it '''
    amenities = []
    all_amenities = storage.all("Amenity")
    for key, val in all_amenities.items():
        amenities.append(val.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_one_amenity(amenity_id=None):
    ''' Gets a dictionary of an amenity and returns it '''
    retrieved_amenity = storage.get("Amenity", amenity_id)
    if retrieved_amenity is None:
        abort(404)
    else:
        return jsonify(retrieved_amenity.to_dict())


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_new_amenity():
    ''' Submits POST request to add a new amenity to the dict of amenities'''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    else:
        if 'name' in data:
            new_amenity = Amenity()
            setattr(new_amenity, 'name', data['name'])
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201
        else:
            abort(400, 'Missing name')


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id=None):
    ''' Deletes a amenity from the dictionary of amenities'''
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def put_to_amenity(amenity_id=None):
    ''' Updates an item in the dictionary of amenities '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    else:
        for key, val in data.items():
            if (key in obj.to_dict() and key not in
                    ['id', 'created_at', 'updated_at']):
                setattr(obj, key, val)
        obj.save()
        return jsonify(obj.to_dict())
