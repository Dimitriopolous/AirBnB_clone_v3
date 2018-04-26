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
from models.city import City
from models.place import Place
import json


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def get_all_places(city_id=None):
    ''' Gets a dictionary of all places then jsonifies and returns it '''
    city_of_places = storage.get("City", city_id)
    if city_of_places is None:
        abort(404)
    places = []
    all_places = storage.all("Place")
    for key, val in all_places.items():
        places.append(val.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_one_place(city_id=None):
    ''' Gets a dictionary of specified place then jsonifies and returns it '''
    retrieved_place = storage.get("Place", place_id)
    if retrieved_place is None:
        abort(404)
    else:
        return jsonify(retrieved_place.to_dict())


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def post_new_place(city_id=None):
    ''' Submits POST request to add a new place to the dictionary of place '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    else:
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        if 'name' in data:
            city_of_new_place = storage.get("City", city_id)
            if city_of_new_place is None:
                abort(404)
            user_owner_of_place = storage.get("User", data['user_id'])
            if user_owner_of_place is None:
                abort(404)
            new_place = Place()
            setattr(new_place, 'name', data['name'])
            setattr(new_place, 'city_id', city_id)
            new_place.save()
            return jsonify(new_place.to_dict()), 201
        else:
            abort(400, 'Missing name')


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id=None):
    ''' Deletes a place from the dictionary of places '''
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        return jsonify({}), 200


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_to_place(place_id=None):
    ''' Updates an item in the dictionary of places '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    else:
        for key, val in data.items():
            if key in obj.to_dict() and key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(obj, key, val)
        obj.save()
        return jsonify(obj.to_dict())

