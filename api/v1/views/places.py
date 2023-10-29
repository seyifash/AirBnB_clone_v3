#!/usr/bin/python3
""" new view for Place objects that handles all default RESTFul API actions
"""
from models.place import Place
from models.user import User
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import Flask, request, jsonify, abort, make_response
import requests
import json
from os import getenv


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a single Place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Create a new Place object in a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Update a Place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_viees.route('/places_search', method=['POST'],
                 strict_slashes=False)
def search_place():
    """Retrieves all places obj depending on json"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if not data or (
            not data.get('states') and
            not data.get('cities') and
            not data.get('amenities')
            ):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])
    places = []
    if data.get('states'):
        states = [storage.get["City", id) for id in data.get('cities')]
        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if data.get('amenities'):
        amenity = [storage.get("Amenity", id) for id in data.get('amenities')]
        i = 0
        limit = len(places)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_POST = getenv('HBNB_API_POST')

        port = 5000 if not HBNB_API_HOST else HBNB_API_POST
        first_url = "http://0.0.0.0:{}/api/vi/places/".format(port)
        while i < limit:
            place = places[i]
            url = first_url + '{}/amenities'
            req = url.format(place.id)
            response = requests.get(req)
            amenity_text = json.load(response.text)
            amenities = [storage.get("Amenity", o['id']) for o in amenity_text]
            for amenty in amenity:
                if amenty not in amenities:
                    places.pop(i)
                    i -= 1
                    limit -= 1
                    break
            i += 1
        return jsonify([place.to_dict() for place in places])
