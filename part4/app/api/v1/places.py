import logging
from flask_restx import Namespace, Resource, fields
from app.api.v1 import facade  # Import the shared facade instance
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

logger = logging.getLogger(__name__)
api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# Add a new model for place updates
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()  # Require authentication to create a new place
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()  # Get the authenticated user's identity
        claims = get_jwt()  # Retrieve all JWT claims
        is_admin = claims.get('is_admin', False)  # Check if user is admin
        place_data = api.payload

        try:
            # Set the owner_id to the authenticated user's ID only if not admin
            if not is_admin:
                place_data['owner_id'] = current_user['id']

            # Create place using the facade
            new_place = facade.create_place(place_data)

            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id,
                'amenities': [amenity.id for amenity in new_place.amenities]
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id,
            'amenities': [amenity.id for amenity in place.amenities]
        } for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id,
            'amenities': [amenity.id for amenity in place.amenities]
        }, 200

    @jwt_required()  # Require authentication to update a place
    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, "Unauthorized action")
    @api.response(400, "Invalid input data")
    def put(self, place_id):
        """Update a place's information (Admins can bypass ownership restrictions)"""
        current_user = get_jwt_identity()  # Get the authenticated user's identity
        claims = get_jwt()  # Retrieve all JWT claims
        is_admin = claims.get('is_admin', False)  # Check if user is admin

        try:
            # Retrieve the existing place
            place = facade.get_place(place_id)
            if not place:
                return {'error': "Place not found"}, 404

            # Ownership check: Admins can bypass this restriction
            if not is_admin and str(place.owner.id) != current_user['id']:
                return {'error': "Unauthorized action"}, 403

            update_data = api.payload
            logger.debug(f"Updating place {place_id} with data: {update_data}")

            # Update the place
            updated_place = facade.update_place(place_id, update_data)

            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner.id,
                'amenities': [amenity.id for amenity in updated_place.amenities]
            }, 200

        except ValueError as e:
            logger.error(f"Validation error while updating place: {str(e)}")
            return {'error': str(e)}, 400
        except Exception as e:
            logger.error(f"Unexpected error while updating place: {str(e)}")
            return {'error': "Internal server error"}, 500

    @jwt_required()  # Require authentication to delete a place
    @api.response(200, "Place deleted successfully")
    @api.response(404, "Place not found")
    @api.response(403, "Unauthorized action")
    def delete(self, place_id):
        """Delete a place (Admins can bypass ownership restrictions)"""
        current_user = get_jwt_identity()  # Get the authenticated user's identity
        claims = get_jwt()  # Retrieve all JWT claims
        is_admin = claims.get('is_admin', False)  # Check if user is admin

        try:
            # Retrieve the existing place
            place = facade.get_place(place_id)
            if not place:
                return {'error': "Place not found"}, 404

            # Ownership check: Admins can bypass this restriction
            if not is_admin and str(place.owner.id) != current_user['id']:
                return {'error': "Unauthorized action"}, 403

            logger.debug(f"Deleting place {place_id}")

            # Delete the place
            facade.delete_place(place_id)

            return {'message': "Place deleted successfully"}, 200

        except Exception as e:
            logger.error(f"Unexpected error while deleting a place: {str(e)}")
            return {'error': "Internal server error"}, 500
