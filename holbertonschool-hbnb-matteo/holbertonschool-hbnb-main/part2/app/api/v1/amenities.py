from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

# Définition du modèle pour l'input et l'output
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = HBnBFacade()

@api.route('/')
class AmenitiesResource(Resource):
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @api.expect(amenity_model)
    def post(self):
        """Create new amenity"""
        data = api.payload
        amenity, error = facade.create_amenity(data)
        if error:
            return {"message": error}, 400
        return amenity.to_dict(), 201

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"message": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update amenity"""
        data = api.payload
        amenity, error = facade.update_amenity(amenity_id, data)
        if error:
            if error == "Amenity not found":
                return {"message": error}, 404
            return {"message": error}, 400
        return amenity.to_dict(), 200