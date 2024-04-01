#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify, request, make_response
from models import storage
from models.state import State
import json


@app_views.route('/states', methods=['GET', 'DELETE', 'POST', 'PUT'])
@app_views.route('/states/<id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
def state(id=None):
    ''' The route the handles the state objects '''

    if request.method == 'GET':

        all = storage.all("State")
        if id is None:

            got = [i.to_dict() for i in all.values()]
            return jsonify(got)

        else:
            state = [state.to_dict() for state in all.values() if state.id == id]
            return jsonify(state[0] if len(state) > 0 else {})


    elif request.method == 'DELETE':
        state = storage.get("State", id)
        if state:
            state.delete()
            storage.save()
            return jsonify({})

        abort(404)
