#!/usr/bin/python3
""" Index module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review

k_list = ["__class__", "created_at", "id", "place_id", "text", "updated_at",
          "user_id"]


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def place_reviews(place_id):
    """ List all available reviews """
    fplace = storage.get(Place, place_id)
    if not fplace:
        abort(404)
    review_list = [{kl: v.to_dict().get(kl) for kl in k_list}
                   for v in fplace.reviews]
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def review(review_id):
    """ Display review with specified id """
    freview = storage.get(Review, review_id)
    if not freview:
        abort(404)
    s_dict = {k: freview.to_dict().get(k) for k in k_list}
    return jsonify(s_dict)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_review(review_id):
    """ Display review with specified id """
    freview = storage.get(Review, review_id)
    if not freview:
        abort(404)
    freview.delete()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new review """
    fplace = storage.get(Place, place_id)
    if not fplace:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "text" not in request.json:
        abort(400, "Missing text")
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    fuser = storage.get("User", reqeust.json["user_id"])
    if not fuser:
        abort(404)
    new_review = Review(name=request.json["text"], place_id=place_id,
                        user_id=request.json["user_id"])
    new_review.save()
    return jsonify({k: new_review.to_dict().get(k) for k in k_list}), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ Updates specified review """
    if not request.json:
        abort(400, "Not a JSON")
    freview = storage.get(Review, review_id)
    if not freview:
        abort(404)
    for key, value in request.json.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(freview, key, value)
    freview.save()
    return jsonify({k: freview.to_dict().get(k) for k in k_list}), 200
