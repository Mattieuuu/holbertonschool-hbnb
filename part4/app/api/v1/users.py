from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.api.v1 import facade  # Import the shared facade instance

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')  # New field for password
})

# Add a model for updating user details (excluding email and password)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})


# Helper function to check admin privileges
def is_admin_user():
    claims = get_jwt()  # Retrieve the JWT claims
    return claims.get('is_admin', False)


@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        return [{'id': user.id,
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email} for user in users], 200

    @api.expect(user_model, validate=True)
    @jwt_required()  # Require authentication to create a new user
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new user (Admin only)"""
        if not is_admin_user():
            return {'error': 'Admin privileges required'}, 403

        from app import bcrypt  # Import différé pour éviter les imports circulaires
        user_data = api.payload

        # Check if email is already in use
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # Hash the password before storing it
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            user_data['password'] = hashed_password

            # Create the new user
            new_user = facade.create_user(user_data)

            # Return only the user's ID and a success message (exclude password)
            return {'id': new_user.id, 'message': 'User successfully created'}, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, id):
        """Get user details by ID"""
        user = facade.get_user(id)
        if not user:
            return {'error': 'User not found'}, 404

        # Exclude the password from the response
        return {'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email}, 200

    @jwt_required()  # Require authentication to update a user's details
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, "You cannot modify email or password")
    @api.response(403, "Unauthorized action")
    def put(self, id):
        """Update user details"""
        current_user = get_jwt_identity()  # Get the authenticated user's identity
        is_admin = is_admin_user()

        # Check if the authenticated user is trying to modify their own details or is an admin
        if not is_admin and str(current_user['id']) != id:
            return {'error': "Unauthorized action"}, 403

        from app import bcrypt  # Import différé pour éviter les imports circulaires
        update_data = api.payload

        # Prevent modification of email and password by regular users
        if not is_admin and ('email' in update_data or 'password' in update_data):
            return {'error': "You cannot modify email or password"}, 400

        try:
            # Update the user's details
            updated_user = facade.update_user(id, update_data)
            if not updated_user:
                return {'error': "User not found"}, 404

            # Exclude the password from the response
            return {'id': updated_user.id,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'email': updated_user.email}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()  # Require authentication to delete a user's account (Admin only)
    @api.response(200, "User successfully deleted")
    @api.response(403, "Admin privileges required")
    def delete(self, id):
        """Delete a user's account (Admin only)"""
        if not is_admin_user():
            return {'error': "Admin privileges required"}, 403

        try:
            deleted = facade.delete_user(id)
            if not deleted:
                return {'error': "User not found"}, 404

            return {'message': "User successfully deleted"}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
