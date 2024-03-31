#!/usr/bin/python3
''' This starts a Flask server/app '''

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_appcontext(code):
    ''' Closes / refreshes the database '''

    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'), port=getenv('HBNB_API_PORT'),
            threaded=True)
