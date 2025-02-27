# app/__init__.py

from flask import Flask
from flask_restx import Api
from app.api.v1.amenities import api as amenities_ns  # Importation du namespace amenities

def create_app():
    # Créer l'application Flask
    app = Flask(__name__)
    
    # Créer une instance de Flask-RESTx API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Enregistrer le namespace des équipements (amenities) dans l'application
    api.add_namespace(amenities_ns, path='/api/v1/amenities')  # Associer le namespace aux routes '/api/v1/amenities'
    
    # Tu peux enregistrer d'autres namespaces ici, si tu en as pour d'autres fonctionnalités (par exemple : utilisateurs, lieux, etc.)

    return app
