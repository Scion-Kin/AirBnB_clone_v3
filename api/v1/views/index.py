#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify

@app_views.route('/status')
def status():
    return jsonify({ 'status': 'OK' })
