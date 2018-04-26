#!/usr/bin/python3
'''
    Module for counting the number of objects in each class
'''
from api.v1.views import app_views
from flask import jsonify
from models import classes, storage


@app_views.route('/status', strict_slashes=False)
def returnStatus():
    ''' return a JSON object with the given key and value '''
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def retrieveNumbers():
    ''' retrieves the number of each object by type '''
    counting_dict = {}
    class_dict = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    for key, value in class_dict.items():
        counting_dict[value] = storage.count(key)
    return jsonify(counting_dict)
