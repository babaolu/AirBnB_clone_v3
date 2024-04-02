#!/usr/bin/python3
""" The index module """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """ Returns server status """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ Stats of each object type """
    all_stats = {
                 "amenities": storage.count("Amenity"),
                 "cities": storage.count("City"),
                 "places": storage.count("Place"),
                 "reviews": storage.count("Review"),
                 "states": storage.count("State"),
                 "users": storage.count("User")
    }
    return jsonify(all_stats)
