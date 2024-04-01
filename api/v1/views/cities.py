#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City


@app_views.route('/cities', methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
@app_views.route('/cities/<id>', methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def city(id=None):
    ''' The route the handles the city objects '''

    if request.method == 'GET':
        all = storage.all("City")
        if id is None:

            got = [i.to_dict() for i in all.values()]
            return jsonify(got)

        else:
            city = ([city for city in all.values() if city.id
                     == id])
            return jsonify(city[0].to_dict() if len(city) > 0 else abort(
                404))

    elif request.method == 'DELETE':
        city = storage.get("City", id) if id else abort(404)
        if city:
            city.delete()
            storage.save()
            return jsonify({})

        abort(404)

    elif request.method == 'POST':
        if not request.get_json() or id:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        else:
            if "name" in request.get_json():
                new = City(**request.get_json())
                new.save()
                return make_response(jsonify(new.to_dict()), 201)

            else:
                return make_response(jsonify({"error": "Missing name"}), 400)

    else:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if not id:
            abort(404)

        all = storage.all("city")
        got = [city for city in all.values() if city.id == id]

        city = got[0] if len(got) > 0 else abort(404)
        for key, value in request.get_json().items():
            if key not in ['created_at', 'updated_at', 'id']:
                setattr(city, key, value)
        city.save()

        return (jsonify(city.to_dict()))
