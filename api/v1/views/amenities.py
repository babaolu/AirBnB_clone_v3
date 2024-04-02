#!/usr/bin/python3
""" The amenities module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity

all_amenities = storage.all(Amenity)
k_list = ["__class__", "created_at", "id", "name", "updated_at"]


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities():
    """ List all available amenities """
    amenity_list = [{kl: v.to_dict().get(kl) for kl in k_list}
                    for k, v in all_amenities.items()]
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Display amenity with specified id """
    famenity = storage.get(Amenity, amenity_id)
    if not famenity:
        abort(404)
    s_dict = {k: famenity.to_dict().get(k) for k in k_list}
    return jsonify(s_dict)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ Display amenity with specified id """
    famenity = storage.get(Amenity, amenity_id)
    if not famenity:
        abort(404)
    famenity.delete()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """ Creates a new amenity """
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    new_amenity = Amenity(name=request.json["name"])
    new_amenity.save()
    return jsonify({k: new_amenity.to_dict().get(k) for k in k_list}), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates specified amenity """
    if not request.json:
        abort(400, "Not a JSON")
    famenity = storage.get(Amenity, amenity_id)
    if not famenity:
        abort(404)
    for key, value in request.json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(famenity, key, value)
    famenity.save()
    return jsonify({k: famenity.to_dict().get(k) for k in k_list}), 200
