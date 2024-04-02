#!/usr/bin/python3
""" Index module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State

k_list = ["__class__", "created_at", "id", "name", "state_id", "updated_at"]


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_cities(state_id):
    """ List all available cities """
    fstate = storage.get(State, state_id)
    if not fstate:
        abort(404)
    city_list = [{kl: v.to_dict().get(kl) for kl in k_list}
                 for v in fstate.cities]
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city(city_id):
    """ Display city with specified id """
    fcity = storage.get(City, city_id)
    if not fcity:
        abort(404)
    s_dict = {k: fcity.to_dict().get(k) for k in k_list}
    return jsonify(s_dict)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_city(city_id):
    """ Display city with specified id """
    fcity = storage.get(City, city_id)
    if not fcity:
        abort(404)
    fcity.delete()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a new city """
    fstate = storage.get(State, state_id)
    if not fstate:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    new_city = City(name=request.json["name"], state_id=state_id)
    new_city.save()
    return jsonify({k: new_city.to_dict().get(k) for k in k_list}), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Updates specified city """
    if not request.json:
        abort(400, "Not a JSON")
    fcity = storage.get(City, city_id)
    if not fcity:
        abort(404)
    for key, value in request.json.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(fcity, key, value)
    fcity.save()
    return jsonify({k: fcity.to_dict().get(k) for k in k_list}), 200
