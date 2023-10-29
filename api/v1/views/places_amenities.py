#!/usr/bin/python3
"""view for the link between Place objects and Amenity objects that
handles all default RESTFul
"""
from models import storage
from models import Place
from models import Amenity
from flask import Flask, abort, make_response, request, jsonify
from api.v1.views import app_views
import os


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place
    """
    amenities = []
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        for amenity in places.amenities:
            amenities.append.amenity.to_dict()
    else:
        for amenity_id in places.amenity_ids:
            amenities.append.storage.get(Amenity, amenity_id).to_dict()
    return jsonify(amenities)


@app_views.route('places/<place_id>/amenities/amenity_id', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_amenities(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in places.amenities:
            abort(404)
        places.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        places.amenity_id.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/amenities/amenity_id', methods=['POST'],
                 strict_slashes=False)
def post_place_amenities(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in places.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        places.amenities.append(amenity)
    else:
        if amenity_id in places.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        places.amenity_ids.append(amenity_id)
    return make_response(jsonify(amenity.to_dict()), 201)
