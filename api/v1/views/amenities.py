#!/usr/bin/python3
''' The amenities blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    all = storage.all("Amenity")
    got = [i.to_dict() for i in all.values()]
    return jsonify(got)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    ''' The route the handles the amenity objects '''

    all = storage.all("Amenity")
    amenity = ([amenity for amenity in all.values()
               if amenity.id == amenity_id])
    return jsonify(amenity[0].to_dict() if len(amenity) > 0 else abort(
        404))


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def destroy(amenity_id):
    amenity = (storage.get("Amenity", amenity_id)
               if amenity_id else abort(404))
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({})

    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    if "name" in request.get_json():
        new = Amenity(**request.get_json())
        new.save()
        return make_response(jsonify(new.to_dict()), 201)

    else:
        return make_response(jsonify({"error": "Missing name"}), 400)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    all = storage.all("Amenity")
    got = [amenity for amenity in all.values() if amenity.id == amenity_id]

    amenity = got[0] if len(got) > 0 else abort(404)
    for key, value in request.get_json().items():
        if key not in ['created_at', 'updated_at', 'id']:
            setattr(amenity, key, value)
    amenity.save()

    return (jsonify(amenity.to_dict()))
