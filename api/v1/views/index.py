#!/usr/bin/python3
""" API Index for Status and Statistics """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns the status of the API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    model_classes = [Amenity, City, Place, Review, State, User]
    model_names = ["amenities", "cities", "places", "reviews", "states", "users"]

    object_counts = {}
    for idx in range(len(classes)):
        object_counts[model_names[idx]] = storage.count(model_classes[idx])

    return jsonify(object_counts)
