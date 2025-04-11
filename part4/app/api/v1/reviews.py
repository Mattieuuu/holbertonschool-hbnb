from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Add a new model for review updates
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()  # Require authentication to create a review
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, "You cannot review your own place")
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()  # Get the authenticated user's identity
        review_data = api.payload

        try:
            # Validate that the user is not reviewing their own place
            place = facade.get_place(review_data['place_id'])
            if int(place.owner.id) == int(current_user['id']):
                return {'error': "You cannot review your own place"}, 403

            # Validate that the user has not already reviewed this place
            if facade.has_already_reviewed(current_user['id'], review_data['place_id']):
                return {'error': "You have already reviewed this place"}, 400

            # Add the user_id to the review data
            review_data['user_id'] = current_user['id']

            # Create the review using the facade
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id,
                 'text': review.text,
                 'rating': review.rating,
                 'user_id': review.user.id,
                 'place_id': review.place.id} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @jwt_required()  # Require authentication to update a review
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, "Unauthorized action")
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()  # Get the authenticated user's identity
        try:
            # Retrieve the existing review
            review = facade.get_review(review_id)
            if not review:
                return {'error': "Review not found"}, 404

            # Check if the current user is the creator of the review
            if str(review.user.id) != current_user['id']:
                return {'error': "Unauthorized action"}, 403

            update_data = api.payload

            # Update the review using the facade
            updated_review = facade.update_review(review_id, update_data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user.id,
                'place_id': updated_review.place.id
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()  # Require authentication to delete a review
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, "Unauthorized action")
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()  # Get the authenticated user's identity
        try:
            # Retrieve the existing review
            review = facade.get_review(review_id)
            if not review:
                return {'error': "Review not found"}, 404

            # Check if the current user is the creator of the review
            if str(review.user.id) != current_user['id']:
                return {'error': "Unauthorized action"}, 403

            # Delete the review using the facade
            if facade.delete_review(review_id):
                return {'message': "Review deleted successfully"}, 200

        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [{'id': review.id,
                     'text': review.text,
                     'rating': review.rating,
                     'user_id': review.user.id} for review in reviews], 200
        except ValueError as e:
            return {'error': str(e)}, 404
