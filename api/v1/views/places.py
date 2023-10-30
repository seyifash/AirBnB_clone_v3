#!/usr/bin/python3
""" View for Place objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
import requests
import json
from os import getenv


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ Deletes a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates a Place object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, description="Not a JSON")
    if "user_id" not in new_place:
        abort(400, description="Missing user_id")
    user_id = new_place['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "name" not in new_place:
        abort(400, description="Missing name")
    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, descriprion="Not a JSON")

    for key, vue in body_request.items():
        if key not in ['id', 'user_id', 'city_at',
                       'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if data is None or not (states or cities or amenities):
        places = storage.all(Place).values()
        result = [place.to_dict() for place in places]
        return jsonify(result)

    the_place = []
    if states:
        the_state = [storage.get(State, the_id) for the_id in states]
        for state in the_state:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            the_place.append(place)

    if cities:
        city_places = []
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                city_places.extend(city.places)
            the_place.extend(city_places)

    if amenities:
        filtered_places = []
        for place in the_place:
            place_amenities = [amenity.id for amenity in place.amenities]
            if set(amenities).issubset(set(place_amenities)):
                filtered_places.append(place)
        the_place = filtered_places
    result = [place.to_dict() for place in the_place]

    return jsonify(result)
