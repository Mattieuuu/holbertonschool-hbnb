from flask_restx import Namespace, Resource, fields
<<<<<<< HEAD
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
=======
from app.services.facade import get_facade

api = Namespace('reviews', description='Review operations')

>>>>>>> mattieu
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

<<<<<<< HEAD
# Model for detailed review information
review_output_model = api.model('ReviewOutput', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place')
})
=======
facade = get_facade()
>>>>>>> mattieu

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
<<<<<<< HEAD
        """Register a new review"""
        try:
            review_data = api.payload
            review = facade.create_review(review_data)
            return review, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
=======
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
>>>>>>> mattieu
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
<<<<<<< HEAD
        review = facade.get_review(review_id)
        if review is None:
            api.abort(404, f"Review with ID {review_id} not found")
        return review, 200
=======
        result, error = facade.get_review(review_id)
        if error:
            return {"message": error}, 404
        return result, 200
>>>>>>> mattieu

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
<<<<<<< HEAD
        """Update a review's information"""
        try:
            review_data = api.payload
            result = facade.update_review(review_id, review_data)
            if result is None:
                api.abort(404, f"Review with ID {review_id} not found")
            return result, 200
        except ValueError as e:
            return {'message': str(e)}, 400
=======
        """Update review"""
        result, error = facade.update_review(review_id, api.payload)
        if error:
            if error == "Review not found":
                return {"message": error}, 404
            return {"message": error}, 400
        return {"message": "Review updated successfully"}, 200
>>>>>>> mattieu

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
<<<<<<< HEAD
        """Delete a review"""
        result = facade.delete_review(review_id)
        if not result:
            api.abort(404, f"Review with ID {review_id} not found")
        return {'message': 'Review deleted successfully'}, 200
=======
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
>>>>>>> mattieu
