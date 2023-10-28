#!/usr/bin/python3
"""State object to handles all default RESTful API"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, Flask, abort, request, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get state information for all states"""
    state_obj = []
    for state in storage.all(State).values():
        state_obj.append(state.to_dict())
    return jsonify(state_obj)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Get by state_id if linked to State or raise 404 error"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """Delete by state_id if linked to State or raise 404 error"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """Create new state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Update a state by id"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in rwquest.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())
