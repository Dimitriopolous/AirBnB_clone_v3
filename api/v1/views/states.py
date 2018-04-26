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
from models.state import State
import json


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_states():
    ''' Gets a dictionary of all states then jsonifies and returns it '''
    states = []
    all_states = storage.all("State")
    for key, val in all_states.items():
        states.append(val.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_one_state(state_id=None):
    ''' Gets a dictionary of specified state then jsonifies and returns it '''
    state = jsonify(storage.get("State", state_id).to_dict())
    if state == None:
        abort(404)
    return state


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_new_state():
    ''' Submits POST request to add a new state to the dictionary of states'''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    else:
        if 'name' in data:
            new_state = State()
            setattr(new_state, 'name', data['name'])
            new_state.save()
            return jsonify(new_state.to_dict()), 201
        else:
            abort(400, 'Missing name')


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id=None):
    ''' Deletes a state from the dictionary of states'''
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        return jsonify({}), 200


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_to_state(state_id=None):
    ''' Updates an item in the dictionary of states '''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    else:
        for key, val in data.items():
            if key in obj.to_dict() and key not in ['id', 'created_at', 'updated_at']:
                setattr(obj, key, val)
        obj.save()
        return jsonify(obj.to_dict())






    


#    @app_views.route('/states/<state_id>', strict_slashes=False,
#                     methods=['GET', 'DELETE', 'PUT'])
#    def httpStates(state_id=None):
#        ''' GETs, POSTs, DELETEs, or PUTs to all State objects '''
#        print("Got into httpStates() method")
#        if request.method == 'GET':
#            print("GET method")
#            if state_id is None or state_id == '':
#                print("No state_id passed")
#                states = []
#                all_states = storage.all("States").values()
#                for item in all_states:
#                    print("Iterating through all_states")
#                    states.append(item.to_dict())
#                return jsonify(states)
#            else:
#                print("Received state_id")
#                state = jsonify(storage.get("State", state_id).to_dict())
#                if state == None:
#                    abort(404)
#                return state
#    
#        elif request.method == 'DELETE':
#            obj = storage.get("State", state_id)
#            if obj is None:
#                abort(404)
#            else:
#                storage.delete(obj)
#                check = jsonify(storage.get("State", state_id).to_dict())       #Verifying if object was successfully deleted
#                return check, 200                                               #If doesn't work we can just return {}
#    
#        elif request.method == 'POST':
#            data = request.get_json()
#            if data is None:
#                abort(400, 'Not a JSON')
#            else:
#                if 'name' in data:
#                    return jsonify(State().to_dict(), 201)
#                else:
#                    abort(400, 'Missing name')
#    
#        elif request.method == 'PUT':
#            data = request.get_json()
#            if data is None:
#                abort(400, 'Not a JSON')
#            obj = storage.get("State", state_id)
#            if obj is None:
#                abort(404)
#            else:
#                for key, val in data.items():
#                    if key in obj and key not in ['id', 'created_at', 'updated_at']:
#                        setattr(obj, key, val)
#                obj.save()
#                    return jsonify(obj.to_dict())
