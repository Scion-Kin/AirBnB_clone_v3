#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    ''' return a status code of OK '''
    return jsonify({'status': 'OK'})


@app_views.route('stats')
def objects():
    ''' retrieves the number of objects by type '''

    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']

    len_all = {}

    for i in classes:

        len_all[i] = storage.count(i)

    return jsonify(len_all)
