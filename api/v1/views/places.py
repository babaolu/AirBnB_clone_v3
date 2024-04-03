#!/usr/bin/python3
""" Index module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place

k_list = ["__class__", "city_id", "created_at", "id", "name", "updated_at",
          "user_id"]


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def city_places(city_id):
    """ List all available places """
    fcity = storage.get(City, city_id)
    if not fcity:
        abort(404)
    place_list = [{kl: v.to_dict().get(kl) for kl in k_list}
                  for v in fcity.places]
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place(place_id):
    """ Display place with specified id """
    fplace = storage.get(Place, place_id)
    if not fplace:
        abort(404)
    s_dict = {k: fplace.to_dict().get(k) for k in k_list}
    return jsonify(s_dict)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_place(place_id):
    """ Display place with specified id """
    fplace = storage.get(Place, place_id)
    if not fplace:
        abort(404)
    fplace.delete()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a new place """
    fcity = storage.get(City, city_id)
    if not fcity:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    fuser = storage.get("User", reqeust.json["user_id"])
    if not fuser:
        abort(404)
    new_place = Place(name=request.json["name"], city_id=city_id,
                      user_id=request.json["user_id"])
    new_place.save()
    return jsonify({k: new_place.to_dict().get(k) for k in k_list}), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ Updates specified place """
    if not request.json:
        abort(400, "Not a JSON")
    fplace = storage.get(Place, place_id)
    if not fplace:
        abort(404)
    for key, value in request.json.items():
        if key not in ["id", "user_id", "city_id", "created_at",
                       "updated_at"]:
            setattr(fplace, key, value)
    fplace.save()
    return jsonify({k: fplace.to_dict().get(k) for k in k_list}), 200
