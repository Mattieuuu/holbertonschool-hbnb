from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Create API with documentation
    api = Api(
        app, 
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Register namespaces with their proper paths
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app