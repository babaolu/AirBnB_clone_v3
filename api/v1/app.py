#!/usr/bin/python3
""" A flask server app """
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception=None):
    """ Cleanup procedures """
    storage.close()


if __name__ == "__main__":
    rhost = getenv("HBNB_API_HOST")
    if not rhost:
        rhost = "0.0.0.0"
    rport = getenv("HBNB_API_PORT")
    if not rport:
        rport = 5000
    app.run(host=rhost, port=rport, threaded=True)
