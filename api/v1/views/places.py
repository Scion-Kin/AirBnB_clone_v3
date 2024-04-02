#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_and_make_places(city_id):
    ''' gets and creates places by a city id'''

    if request.method == 'GET':
        city = [city for city in storage.all("City").values()
                if city.id == city_id]
        if len(city) < 1:
            abort(404)

        places = ([place.to_dict() for place in
                  storage.all("Place").values() if place.city_id == city_id])
        return jsonify(places) if len(places) > 0 else jsonify([])

    elif request.method == 'POST' and request.get_json():
        ''' create a new place '''
        city = [city for city in storage.all("City").values()
                if city.id == city_id]
        if len(city) < 1:
            abort(404)

        if "user_id" not in request.get_json():
            return make_response(jsonify({"error": "Missing user_id"}), 400)

        user = [user for user in storage.all("User").values()
                if user.id == request.get_json()['user_id']]
        if len(user) < 1:
            abort(404)

        if "name" in request.get_json():
            new = Place(city_id=city_id, **request.get_json())
            new.save()
            return make_response(jsonify(new.to_dict()), 201)

        else:
            return make_response(jsonify({"error": "Missing name"}), 400)


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_destroy_and_update_places(place_id):
    ''' Gets, deletes and updates a place by its id '''

    if request.method == 'GET':
        all = storage.all("Place")
        all = [place for place in all.values() if place.id == place_id]

        return jsonify(all[0].to_dict()) if len(all) > 0 else abort(404)

    if request.method == 'DELETE':
        ''' Deletes a place from a database '''

        all = storage.all("Place")
        all = [place for place in all.values() if place.id == place_id]
        place = all[0] if len(all) > 0 else abort(404)
        place.delete()
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        ''' updates a place in the database '''
        if request.get_json():
            all = storage.all("Place")
            got = [place for place in all.values() if place.id == place_id]

            place = got[0] if len(got) > 0 else abort(404)
            for key, value in request.get_json().items():
                if key not in ['created_at', 'updated_at',
                               'city_id', 'id', 'user_id']:
                    setattr(place, key, value)
            place.save()

            return (jsonify(place.to_dict()))
