from flask_restx import Namespace, Resource, fields
from app.services.facade import get_facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

facade = get_facade()

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        result, error = facade.create_review(api.payload)
        if error:
            return {"message": error}, 400
        return result, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get all reviews"""
        return facade.get_all_reviews(), 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        result, error = facade.get_review(review_id)
        if error:
            return {"message": error}, 404
        return result, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review"""
        result, error = facade.update_review(review_id, api.payload)
        if error:
            if error == "Review not found":
                return {"message": error}, 404
            return {"message": error}, 400
        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review"""
        error = facade.delete_review(review_id)
        if error:
            return {"message": error}, 404
        return {"message": "Review deleted successfully"}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a place"""
        result, error = facade.get_reviews_by_place(place_id)
        if error:
            return {"message": error}, 404
        return result, 200
