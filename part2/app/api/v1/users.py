from flask_restx import Namespace, Resource, fields
from app.services.facade import get_facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User unique identifier'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

# Use the get_facade function to get an instance of HBnBFacade
facade_instance = get_facade()

@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """List all users"""
        return facade_instance.get_users(), 200

    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    def post(self):
        """Create a new user"""
        user, error = facade_instance.create_user(api.payload)
        if error:
            return {"message": error}, 400
        return user, 201

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class User(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID"""
        user, error = facade_instance.get_user(user_id)
        if error:
            return {"message": error}, 404
        return user, 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update a user"""
        user, error = facade_instance.update_user(user_id, api.payload)
        if error:
            if error == "User not found":
                return {"message": error}, 404
            return {"message": error}, 400
        return user, 200