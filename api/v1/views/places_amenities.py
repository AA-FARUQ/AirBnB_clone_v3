#!/usr/bin/python3
""" Handles all default RestFul API actions for place - Amenity relationships"""
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['GET'])
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place_instance = storage.get(Place, place_id)

    if not place_instance:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place_instance.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities.yml',
           methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object of a Place
    """
    place_instance = storage.get(Place, place_id)

    if not place_instance:
        abort(404)

    amenity_instance = storage.get(Amenity, amenity_id)

    if not amenity_instance:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity_instance not in place_instance.amenities:
            abort(404)
        place_instance.amenities.remove(amenity_instance)
    else:
        if amenity_id not in place_instance.amenity_ids:
            abort(404)
        place_instance.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities.yml',
           methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place
    """
    place_instance = storage.get(Place, place_id)

    if not place_instance:
        abort(404)

    amenity_instance = storage.get(Amenity, amenity_id)

    if not amenity_instance:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity_instance in place_instance.amenities:
            return make_response(jsonify(amenity_instance.to_dict()), 200)
        else:
            place_instance.amenities.append(amenity_instance)
    else:
        if amenity_id in place_instance.amenity_ids:
            return make_response(jsonify(amenity_instance.to_dict()), 200)
        else:
            place_instance.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity_instance.to_dict()), 201)
