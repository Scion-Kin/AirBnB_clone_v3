#!/usr/bin/python3
''' The reviews blueprint '''
from api.v1.views import app_views
from flask import Flask, Blueprint
from flask import jsonify, request, abort, make_response
from models import storage
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_and_make_reviews(place_id):
    ''' gets and creates reviews by a place id'''

    if request.method == 'GET':
        place = [place for place in storage.all("Place").values()
                 if place.id == place_id]
        if len(place) < 1:
            abort(404)

        reviews = ([review.to_dict() for review in
                   storage.all("Review").values()
                   if review.place_id == place_id])
        return jsonify(reviews) if len(reviews) > 0 else jsonify([])

    elif request.method == 'POST':
        ''' create a new review '''
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        place = [place for place in storage.all("Place").values()
                 if place.id == place_id]
        if len(place) < 1:
            abort(404)

        if "user_id" not in request.get_json():
            return make_response(jsonify({"error": "Missing user_id"}), 400)

        user = [user for user in storage.all("User").values()
                if user.id == request.get_json()['user_id']]
        if len(user) < 1:
            abort(404)

        if "text" in request.get_json():
            new = Review(place_id=place_id, **request.get_json())
            new.save()
            return make_response(jsonify(new.to_dict()), 201)

        else:
            return make_response(jsonify({"error": "Missing text"}), 400)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_destroy_and_update_reviews(review_id):
    ''' Gets, deletes and updates a review by its id '''

    if request.method == 'GET':
        all = storage.all("Review")
        all = [review for review in all.values() if review.id == review_id]

        return jsonify(all[0].to_dict()) if len(all) > 0 else abort(404)

    if request.method == 'DELETE':
        ''' Deletes a review from a database '''

        all = storage.all("Review")
        all = [review for review in all.values() if review.id == review_id]
        review = all[0] if len(all) > 0 else abort(404)
        review.delete()
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        ''' updates a review in the database '''

        if request.get_json():
            all = storage.all("Review")
            got = [review for review in all.values() if review.id == review_id]

            review = got[0] if len(got) > 0 else abort(404)
            for key, value in request.get_json().items():
                if key not in ['created_at', 'updated_at',
                               'place_id', 'id', 'user_id']:
                    setattr(review, key, value)
            review.save()

            return (jsonify(review.to_dict()))

        return make_response(jsonify({"error": "Not a JSON"}), 400)
