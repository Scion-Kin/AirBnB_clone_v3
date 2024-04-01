#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
@app_views.route('/states/<id>', methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def state(id=None):
    ''' The route the handles the state objects '''

    if request.method == 'GET':
        all = storage.all("State")
        if id is None:

            got = [i.to_dict() for i in all.values()]
            return jsonify(got)

        else:
            state = ([state.to_dict() for state in all.values() if state.id
                     == id])
            return jsonify(state[0] if len(state) > 0 else abort(404))

    elif request.method == 'DELETE':
        state = storage.get("State", id) if id else abort(404)
        if state:
            state.delete()
            storage.save()
            return jsonify({})

        abort(404)

    elif request.method == 'POST':
        if not request.get_json() or id:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        else:
            if "name" in request.get_json():
                new = State(**request.get_json())
                new.save()
                return new.to_dict()

            else:
                return make_response(jsonify({"error": "Missing name"}), 400)

    else:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if not id:
            abort(404)

        all = storage.all("State")
        got = [state for state in all.values() if state.id == id]

        state = got[0] if len(got) > 0 else abort(404)
        for key, value in request.get_json().items():
            if key not in ['created_at', 'updated_at', 'id']:
                setattr(state, key, value)
        state.save()

        return (jsonify(state.to_dict()))
