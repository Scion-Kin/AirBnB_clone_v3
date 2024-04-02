#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def amenity(amenity_id=None):
    ''' The route the handles the amenity objects '''

    if request.method == 'GET':
        all = storage.all("Amenity")
        if amenity_id is None:

            got = [i.to_dict() for i in all.values()]
            return jsonify(got)

        else:
            amenity = ([amenity for amenity in all.values()
                       if amenity.id == amenity_id])
            return jsonify(amenity[0].to_dict() if len(amenity) > 0 else abort(
                404))

    elif request.method == 'DELETE':
        amenity = (storage.get("Amenity", amenity_id)
                   if amenity_id else abort(404))
        if amenity:
            amenity.delete()
            storage.save()
            return jsonify({})

        abort(404)

    elif request.method == 'POST':
        print(request.get_json())
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        else:
            if "name" in request.get_json():
                new = Amenity(**request.get_json())
                new.save()
                return make_response(jsonify(new.to_dict()), 201)

            else:
                return make_response(jsonify({"error": "Missing name"}), 400)

    else:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if not amenity_id:
            abort(404)

        all = storage.all("Amenity")
        got = [amenity for amenity in all.values() if amenity.id == amenity_id]

        amenity = got[0] if len(got) > 0 else abort(404)
        for key, value in request.get_json().items():
            if key not in ['created_at', 'updated_at', 'id']:
                setattr(amenity, key, value)
        amenity.save()

        return (jsonify(amenity.to_dict()))

@app_views.errorhandler(415)
def not_a_json(error):
    return make_response(jsonify({"error": "Not a JSON"}), 400)
