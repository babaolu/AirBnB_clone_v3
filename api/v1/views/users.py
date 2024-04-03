#!/usr/bin/python3
""" The users module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User

all_users = storage.all(User)
k_list = ["__class__", "created_at", "email", "id", "password", "updated_at"]


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    """ List all available users """
    user_list = [{kl: v.to_dict().get(kl) for kl in k_list}
                 for k, v in all_users.items()]
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user(user_id):
    """ Display user with specified id """
    fuser = storage.get(User, user_id)
    if not fuser:
        abort(404)
    s_dict = {k: fuser.to_dict().get(k) for k in k_list}
    return jsonify(s_dict)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_user(user_id):
    """ Display user with specified id """
    fuser = storage.get(User, user_id)
    if not fuser:
        abort(404)
    fuser.delete()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """ Creates a new user """
    if not request.json:
        abort(400, "Not a JSON")
    if "email" not in request.json:
        abort(400, "Missing email")
    if "password" not in request.json:
        abort(400, "Missing password")
    new_user = User(email=request.json["email"],
                    password=request.json["password"])
    new_user.save()
    return jsonify({k: new_user.to_dict().get(k) for k in k_list}), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ Updates specified user """
    if not request.json:
        abort(400, "Not a JSON")
    fuser = storage.get(User, user_id)
    if not fuser:
        abort(404)
    for key, value in request.json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(fuser, key, value)
    fuser.save()
    return jsonify({k: fuser.to_dict().get(k) for k in k_list}), 200
