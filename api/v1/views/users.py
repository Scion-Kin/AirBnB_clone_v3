#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def user(user_id=None):
    ''' The route the handles the user objects '''

    if request.method == 'GET':
        all = storage.all("User")
        if user_id is None:

            got = [i.to_dict() for i in all.values()]
            return jsonify(got)

        else:
            user = ([user for user in all.values()
                    if user.id == user_id])
            return jsonify(user[0].to_dict() if len(user) > 0 else abort(
                404))

    elif request.method == 'DELETE':
        user = (storage.get("User", user_id)
                if user_id else abort(404))
        if user:
            user.delete()
            storage.save()
            return jsonify({})

        else:
            abort(404)

    elif request.method == 'POST':
        if not request.get_json() or user_id:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        else:
            if "email" not in request.get_json():
                return make_response(jsonify({"error": "Missing email"}), 400)

            if "password" not in request.get_json():
                return make_response(jsonify(
                    {"error": "Missing password"}), 400)

            new = User(**request.get_json())
            new.save()
            return make_response(jsonify(new.to_dict()), 201)

    else:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if not user_id:
            abort(404)

        all = storage.all("User")
        got = [user for user in all.values() if user.id == user_id]

        user = got[0] if len(got) > 0 else abort(404)
        for key, value in request.get_json().items():
            if key not in ['created_at', 'updated_at', 'id', 'email']:
                setattr(user, key, value)
        user.save()

        return (jsonify(user.to_dict()))
