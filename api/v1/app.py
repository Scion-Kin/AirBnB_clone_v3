#!/usr/bin/python3
''' This starts a Flask server/app '''

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
CORS(app)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_appcontext(code):
    ''' Closes / refreshes the database '''

    storage.close()


@app.errorhandler(404)
def not_found(error):
    ''' Returns a not found JSON, on not found pages '''

    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'), port=getenv('HBNB_API_PORT'),
            threaded=True)
