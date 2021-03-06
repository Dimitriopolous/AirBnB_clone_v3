#!/usr/bin/python3
'''
    views for RESTful API
    HTTP requests that allow users
    to manipulate data in storage
'''

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import classes, storage
from models.city import City
from models.state import State
import json


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_all_cities(state_id=None):
    ''' Gets a dictionary of all cities then jsonifies and returns it '''
    state_of_cities = storage.get("State", state_id)
    if state_of_cities is None:
        abort(404)
    cities = []
    all_cities = storage.all("City")
    for key, val in all_cities.items():
        cities.append(val.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_one_city(city_id=None):
    ''' Gets a dictionary of specified city then jsonifies and returns it '''
    retrieved_city = storage.get("City", city_id)
    if retrieved_city is None:
        abort(404)
    else:
        return jsonify(retrieved_city.to_dict())


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def post_new_city(state_id=None):
    ''' Submits POST request to add a new city to the dictionary of cities '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    else:
        if 'name' in data:
            state_of_new_city = storage.get("State", state_id)
            if state_of_new_city is None:
                abort(404)
            new_city = City()
            setattr(new_city, 'name', data['name'])
            setattr(new_city, 'state_id', state_id)
            new_city.save()
            return jsonify(new_city.to_dict()), 201
        else:
            abort(400, 'Missing name')


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id=None):
    ''' Deletes a city from the dictionary of cities '''
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        return jsonify({}), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_to_city(city_id=None):
    ''' Updates an item in the dictionary of states '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    else:
        for key, val in data.items():
            if (key in obj.to_dict() and key not in
                    ['id', 'state_id', 'created_at', 'updated_at']):
                setattr(obj, key, val)
        obj.save()
        return jsonify(obj.to_dict())
