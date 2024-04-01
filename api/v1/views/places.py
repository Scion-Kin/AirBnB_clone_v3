#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_places(city_id):
    ''' gets all places by a city id '''

    if request.method == 'GET':
        places = ([place.to_dict() for place in
                  storage.all("place").values() if place.city_id == city_id])
        return jsonify(places) if len(places) > 0 else abort(404)

    else:

        if not request.get_json() or not city_id:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if "user_id" not in request.get_json():
            return make_response(jsonify({"error": "Missing user_id"}), 400)

        else:
            user_exists = ([user for user in storage.all("User")
                           if user.id == request.get_json()['user_id']])
            city_exists = ([city for city in storage.all(
                           "City") if city.id == city_id])
            if len(city_exists) < 1 and len(user_exists) < 1:
                abort(404)
            if "name" in request.get_json():
                new = place(city_id=city_id, **request.get_json())
                new.save()
                return make_response(jsonify(new.to_dict()), 201)

            else:
                return make_response(jsonify({"error": "Missing name"}), 400)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT'],
                 strict_slashes=False)
def get_place(place_id):
    ''' Gets a place by its id '''

    if request.method == 'GET':
        all = storage.all("place")
        all = [place for place in all.values() if place.id == place_id]

        return jsonify(all[0].to_dict()) if len(all) > 0 else abort(404)

    elif request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if not place_id:
            abort(404)

        all = storage.all("place")
        got = [place for place in all.values() if place.id == place_id]

        place = got[0] if len(got) > 0 else abort(404)
        for key, value in request.get_json().items():
            if key not in ['created_at', 'updated_at',
                           'id', 'user_id', 'city_id']:
                setattr(place, key, value)
        place.save()

        return (jsonify(place.to_dict()))

    else:
        all = storage.all("place")
        all = [place for place in all.values() if place.id == place_id]
        place = all[0] if len(all) > 0 else abort(404)
        place.delete()
        storage.save()
        return jsonify({})
