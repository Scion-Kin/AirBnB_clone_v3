#!/usr/bin/python3
''' The cities blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    ''' gets all cities by a state id '''

    state = [state for state in storage.all("State").values()
             if state.id == state_id]
    if len(state) < 1:
        abort(404)

    cities = ([city.to_dict() for city in
              storage.all("City").values() if city.state_id == state_id])
    return jsonify(cities) if len(cities) > 0 else jsonify([])


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    ''' Gets a city by its id '''

    all = storage.all("City")
    all = [city for city in all.values() if city.id == city_id]

    return jsonify(all[0].to_dict()) if len(all) > 0 else abort(404)


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def destroy_city(city_id):
    ''' Deletes a city from a database '''

    all = storage.all("City")
    all = [city for city in all.values() if city.id == city_id]
    city = all[0] if len(all) > 0 else abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create(state_id):
    ''' create a new city '''
    state = [state for state in storage.all("State").values()
             if state.id == state_id]
    if len(state) < 1:
        abort(404)

    if "name" in request.get_json():
        new = City(state_id=state_id, **request.get_json())
        new.save()
        return make_response(jsonify(new.to_dict()), 201)

    else:
        return make_response(jsonify({"error": "Missing name"}), 400)


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'], strict_slashes=False)
def update(city_id):
    ''' updates a city in the database '''

    if not city_id:
        abort(404)

    all = storage.all("City")
    got = [city for city in all.values() if city.id == city_id]

    city = got[0] if len(got) > 0 else abort(404)
    for key, value in request.get_json().items():
        if key not in ['created_at', 'updated_at', 'id']:
            setattr(city, key, value)
    city.save()

    return (jsonify(city.to_dict()))
