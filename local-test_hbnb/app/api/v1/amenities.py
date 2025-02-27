# api/v1/amenities.py

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Operations related to amenities')

# Modèle de validation d'entrée pour les équipements
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')  # Attribut "name" requis
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload  # Récupérer les données envoyées dans la requête

        new_amenity = facade.create_amenity(amenity_data)  # Créer l'équipement via la couche logique
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201  # Retourner l'équipement créé

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()  # Récupérer tous les équipements
        return [{'id': amenity.id, 'name': amenity.name} for amenity in amenities], 200  # Retourner la liste des équipements

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)  # Récupérer un équipement par ID
        if not amenity:
            return {'error': 'Amenity not found'}, 404  # Si l'équipement n'existe pas
        return {'id': amenity.id, 'name': amenity.name}, 200  # Retourner les détails de l'équipement

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload  # Récupérer les nouvelles données
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)  # Mettre à jour l'équipement
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404  # Si l'équipement n'existe pas
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200  # Retourner l'équipement mis à jour
