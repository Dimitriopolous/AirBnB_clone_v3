#!/usr/bin/python3
'''
    Blueprint app_views decorators
    for HTTP requests to the Review class
    which allows users to manipulate
    data in storage
'''

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import classes, storage
from models.place import Place
from models.review import Review
import json


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_all_reviews(place_id=None):
    ''' Gets a dictionary of all reviews and returns it '''
    place_of_reviews = storage.get("Place", place_id)
    if place_of_reviews is None:
        abort(404)
    reviews = []
    all_reviews = storage.all("Review")
    for key, val in all_reviews.items():
        reviews.append(val.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def get_one_review(review_id=None):
    ''' Gets a dictionary of specified review and returns it '''
    retrieved_review = storage.get("Review", review_id)
    if retrieved_review is None:
        abort(404)
    else:
        return jsonify(retrieved_review.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def post_new_review(place_id=None):
    '''
    Submits POST request to add a new
    review to the dictionary of review
    '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    else:
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        if 'text' in data:
            place_of_new_review = storage.get("Place", place_id)
            if place_of_new_review is None:
                abort(404)
            owner_of_review = storage.get("User", data['user_id'])
            if owner_of_review is None:
                abort(404)
            new_review = Review()
            setattr(new_review, 'user_id', data['user_id'])
            setattr(new_review, 'text', data['text'])
            setattr(new_review, 'place_id', place_id)
            new_review.save()
            return jsonify(new_review.to_dict()), 201
        else:
            abort(400, 'Missing text')


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id=None):
    ''' Deletes a review from the dictionary of reviews '''
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        return jsonify({}), 200


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def put_to_review(review_id=None):
    ''' Updates an item in the dictionary of reviews '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    else:
        for key, val in data.items():
            if (key in obj.to_dict() and key not in
                    ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']):
                setattr(obj, key, val)
        obj.save()
        return jsonify(obj.to_dict())
