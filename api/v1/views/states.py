#!/usr/bin/python3
""" Index module """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State

all_states = storage.all(State)
k_list = ["__class__", "created_at", "id", "name", "updated_at"]


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """ List all available states """
    state_list = [{kl: v.to_dict().get(kl) for kl in k_list}
                  for k, v in all_states.items()]
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state(state_id):
    """ Display state with specified id """
    fstate = all_states.get("State." + state_id, None)
    if not fstate:
        abort(404)
    s_dict = {k: fstate.to_dict().get(k) for k in k_list}
    return jsonify(s_dict)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_state(state_id):
    """ Display state with specified id """
    fstate = all_states.pop("State." + state_id, None)
    if not fstate:
        abort(404)
    storage.delete(fstate)
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Creates a new state """
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    new_state = State(name=request.json["name"])
    new_state.save()
    return jsonify({k: new_state.to_dict().get(k) for k in k_list}), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ Updates specified state """
    if not request.json:
        abort(400, "Not a JSON")
    fstate = all_states.get("State." + state_id, None)
    if not fstate:
        abort(404)
    for key, value in request.json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fstate, key, value)
    fstate.save()
    return jsonify({k: fstate.to_dict().get(k) for k in k_list}), 200
