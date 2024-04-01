#!/usr/bin/python3
""" Index module """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """ Server status """
    return jsonify({
                       "status": "OK"
                    })


@app_views.route("/stats")
def stats():
    """ Stats of each object type """
    all_stats = {
    "amenities": storage.count("Amenity"),
    "cities": storage.count("City"),
    "reviews": storage.count("Review"),
    "states": storage.count("State"),
    "users": storage.count("User")
    }
    return jsonify(all_stats)
