#!/usr/bin/python3
''' The index of the blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify, request, abort, make_response
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_reviews(place_id):
    ''' gets all reviews by a place id '''

    if request.method == 'GET':
        reviews = ([review.to_dict() for review in
                   storage.all("Review").values()
                   if review.place_id == place_id])
        return jsonify(reviews) if len(reviews) > 0 else abort(404)

    else:

        if not request.get_json() or not place_id:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if "user_id" not in request.get_json():
            return make_response(jsonify({"error": "Missing user_id"}), 400)

        else:
            user_exists = ([user for user in storage.all("User")
                           if user.id == request.get_json()['user_id']])
            place_exists = ([place for place in storage.all(
                           "Place") if place.id == place_id])
            if len(place_exists) < 1 and len(user_exists) < 1:
                abort(404)
            if "name" in request.get_json():
                new = review(place_id=place_id, **request.get_json())
                new.save()
                return make_response(jsonify(new.to_dict()), 201)

            else:
                return make_response(jsonify({"error": "Missing name"}), 400)


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT'],
                 strict_slashes=False)
def get_review(review_id):
    ''' Gets a review by its id '''

    if request.method == 'GET':
        all = storage.all("Review")
        all = [review for review in all.values() if review.id == review_id]

        return jsonify(all[0].to_dict()) if len(all) > 0 else abort(404)

    elif request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        if not review_id:
            abort(404)

        all = storage.all("Review")
        got = [review for review in all.values() if review.id == review_id]

        review = got[0] if len(got) > 0 else abort(404)
        for key, value in request.get_json().items():
            if key not in ['created_at', 'updated_at',
                           'id', 'user_id', 'place_id']:
                setattr(review, key, value)
        review.save()

        return (jsonify(review.to_dict()))

    else:
        all = storage.all("Review")
        all = [review for review in all.values() if review.id == review_id]
        review = all[0] if len(all) > 0 else abort(404)
        review.delete()
        storage.save()
        return jsonify({})
