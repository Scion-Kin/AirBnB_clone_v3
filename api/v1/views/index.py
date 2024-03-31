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

    classes = {'Amenity': 'amenities', 'City': 'cities',
               'Place': 'places', 'Review': 'reviews',
               'State': 'states', 'User': 'users'}

    len_all = {}

    for i in classes:

        len_all[classes[i]] = storage.count(i)

    return jsonify(len_all)
