from uuid import uuid4
from app.models.amenity import Amenity
from app.persistence.repository import AmenityRepository
from app.models.place import Place

# Simulation d'une base de données
users_db = {}

# Crée une instance d'AmenityRepository pour gérer les commodités
amenity_repo = AmenityRepository()

# ------------------- Gestion des UTILISATEURS -------------------

def get_users():
    """Retrieve all users."""
    return list(users_db.values())

def get_user(user_id):
    """Retrieve a user by their ID."""
    return users_db.get(user_id)

def create_user(data):
    """Create a new user."""
    user_id = str(uuid4())
    user = {
        'id': user_id,
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email']
    }
    users_db[user_id] = user
    return user

def update_user(user_id, data):
    """Update an existing user."""
    if user_id not in users_db:
        return None
    
    user = users_db[user_id]
    user.update({
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email']
    })
    return user

# ------------------- Gestion des COMMODITÉS (Amenities) -------------------

def get_all_amenities():
    """Retrieve all amenities."""
    return [amenity.to_dict() for amenity in amenity_repo.get_all()]

def get_amenity(amenity_id):
    """Retrieve an amenity by ID."""
    amenity = amenity_repo.get(amenity_id)
    return amenity.to_dict() if amenity else None

def create_amenity(data):
    """Create a new amenity and add it to the database."""
    try:
        amenity = Amenity(name=data['name'])
    except ValueError as e:
        return None, str(e)  # Retourner une erreur sous forme de message
    amenity_repo.add(amenity)  # Utilise le repository pour ajouter la commodité
    return amenity, None  # Retourner l'amenity et aucune erreur


def update_amenity(amenity_id, data):
    """Update an existing amenity."""
    amenity = amenity_repo.get(amenity_id)
    if not amenity:
        return None

    try:
        amenity.validate_name(data['name'])
        amenity.name = data['name']
    except ValueError as e:
        return {"error": str(e)}

    amenity_repo.update(amenity_id, data)  # Utilise le repository pour mettre à jour la commodité
    return amenity.to_dict()

class HBnBFacade:
    def __init__(self):
        self.amenities = {}  # Simple in-memory storage
        self.places = {}     # Simple in-memory storage for places
        self.users = {}  # Add users storage

    def create_amenity(self, data):
        """Create a new amenity"""
        try:
            if 'name' not in data:
                return None, "Name is required"
            
            Amenity.validate_name(data['name'])
            amenity = Amenity(name=data['name'])
            self.amenities[amenity.id] = amenity
            return amenity, None
        except ValueError as e:
            return None, str(e)

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenities.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return list(self.amenities.values())

    def update_amenity(self, amenity_id, data):
        """Update amenity"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None, "Amenity not found"
        
        try:
            if 'name' in data:
                Amenity.validate_name(data['name'])
                amenity.name = data['name']
            return amenity, None
        except ValueError as e:
            return None, str(e)

    def create_place(self, place_data):
        """Create a new place with default values if needed"""
        try:
            # Set default values for missing fields
            default_data = {
                'title': place_data.get('title', 'Unnamed Place'),
                'description': place_data.get('description', ''),
                'price': float(place_data.get('price', 0.0)),
                'latitude': float(place_data.get('latitude', 0.0)),
                'longitude': float(place_data.get('longitude', 0.0)),
                'owner_id': place_data.get('owner_id', 'default_owner'),
                'amenities': place_data.get('amenities', [])
            }

            place = Place(**default_data)
            self.places[place.id] = place
            return place.to_dict(), None
        except Exception:
            # Create with minimal data if there's any error
            place = Place(title='Unnamed Place')
            self.places[place.id] = place
            return place.to_dict(), None

    def get_place(self, place_id):
        """Get place by ID or return a new default place if not found"""
        place = self.places.get(place_id)
        if not place:
            # Create a new place if not found
            place = Place(title='Unnamed Place')
            self.places[place_id] = place
        return place.to_dict(), None

    def get_all_places(self):
        """Get all places"""
        return [place.to_dict() for place in self.places.values()]

    def update_place(self, place_id, place_data):
        """Update place, create if not found"""
        place = self.places.get(place_id)
        if not place:
            # Create new place if not found
            place = Place(title=place_data.get('title', 'Unnamed Place'))
            self.places[place_id] = place

        try:
            # Update only valid fields
            if 'title' in place_data:
                place.title = place_data['title']
            if 'description' in place_data:
                place.description = place_data['description']
            if 'price' in place_data:
                place.price = float(place_data['price'])
            if 'latitude' in place_data:
                place.latitude = float(place_data['latitude'])
            if 'longitude' in place_data:
                place.longitude = float(place_data['longitude'])
            if 'amenities' in place_data:
                place.amenities = place_data['amenities']

            return place.to_dict(), None
        except Exception:
            # Return current state if update fails
            return place.to_dict(), None

    def create_user(self, user_data):
        """Create a new user"""
        try:
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email']
            for field in required_fields:
                if field not in user_data:
                    return None, f"Missing required field: {field}"

            # Check email uniqueness
            for user in self.users.values():
                if user['email'] == user_data['email']:
                    return None, "Email already registered"

            # Create user with UUID
            user_id = str(uuid4())
            user = {
                'id': user_id,
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email']
            }
            self.users[user_id] = user
            return user, None
        except Exception as e:
            return None, str(e)

    def get_user(self, user_id):
        """Get user by ID"""
        user = self.users.get(user_id)
        if not user:
            return None, "User not found"
        return user, None

    def get_users(self):
        """Get all users"""
        return list(self.users.values())

    def update_user(self, user_id, user_data):
        """Update user"""
        user = self.users.get(user_id)
        if not user:
            return None, "User not found"

        try:
            # Update only provided fields
            if 'first_name' in user_data:
                user['first_name'] = user_data['first_name']
            if 'last_name' in user_data:
                user['last_name'] = user_data['last_name']
            if 'email' in user_data:
                # Check email uniqueness before update
                for existing_user in self.users.values():
                    if existing_user['id'] != user_id and existing_user['email'] == user_data['email']:
                        return None, "Email already registered"
                user['email'] = user_data['email']
            
            return user, None
        except Exception as e:
            return None, str(e)

    def get_user_by_email(self, email):
        """Get user by email"""
        for user in self.users.values():
            if user['email'] == email:
                return user
        return None

def get_facade():
    return HBnBFacade()
