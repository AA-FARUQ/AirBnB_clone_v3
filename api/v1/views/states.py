#!/usr/bin/python3
"""Handles all default RestFul API actions for States """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(State).values()
    list_states = []
    for state_instance in all_states:
        states_list.append(state_instance.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def get_state(state_id):
    """ Retrieves a specific State """
    state_instance = storage.get(State, state_id)
    if not state_instance:
        abort(404)

    return jsonify(state_instance.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State Object
    """

    state_instance = storage.get(State, state_id)

    if not state_instance:
        abort(404)

    storage.delete(state_instance)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def post_state():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    state_data = request.get_json()
    new_state = State(**state_data)
    new_state.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def put_state(state_id):
    """
    Updates an existing State
    """
    state_instance = storage.get(State, state_id)

    if not state_instance:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_fields = ['id', 'created_at', 'updated_at']

    update_data = request.get_json()
    for key, value in update_data.items():
        if key not in ignore_fields:
            setattr(state_instance, key, value)
    storage.save()
    return make_response(jsonify(state_instance.to_dict()), 200)