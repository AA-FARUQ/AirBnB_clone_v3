#!/usr/bin/python3
""" Handles all default RestFul API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves a list of all user objects
    """
    all_users = storage.all(User).values()
    users_list = []
    for user_instance in all_users:
        users_list.append(user_instance.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """ Retrieves a specific user by ID """
    user_instance = storage.get(User, user_id)
    if not user_instance:
        abort(404)

    return jsonify(user_instance.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)

    if not user_instance:
        abort(404)

    storage.delete(user_instance)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def post_user():
    """
    Creates a new user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    user_data = request.get_json()
    new_user = User(**user_data)
    new_user.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """
    Updates an existing user
    """
    user_instance = storage.get(User, user_id)

    if not user_instance:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_fields = ['id', 'email', 'created_at', 'updated_at']

    update_data = request.get_json()
    for key, value in update_data.items():
        if key not in ignore_fields:
            setattr(user_instance, key, value)
    storage.save()
    return make_response(jsonify(user_instance.to_dict()), 200)
