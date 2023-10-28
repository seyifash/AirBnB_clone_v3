#!/usr/bin/python3
"""state obj that handles all default RESTful API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get state information for all states"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """get state information for specified state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """deletes a state based on its state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """create a new state"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """update a state"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()))
