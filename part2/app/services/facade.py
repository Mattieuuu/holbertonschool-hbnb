"""
Le pattern Façade (Facade) est un patron de conception qui fournit une interface simplifiée
à un ensemble complexe de classes, une bibliothèque ou un framework.

Imaginez un restaurant : le serveur est une façade entre vous (le client) et tout le système
complexe de la cuisine (chefs, plongeurs, etc.). Vous n'avez pas besoin de connaître tous
les détails de la cuisine pour commander un plat.

Dans ce fichier :
- uuid4() : Génère des identifiants uniques aléatoires, comme '550e8400-e29b-41d4-a716-446655440000'
- **data : L'opérateur ** "décompresse" un dictionnaire. Par exemple:
    data = {'name': 'John', 'age': 30}
    function(**data) équivaut à function(name='John', age=30)
"""

# Importation des modules nécessaires
from uuid import uuid4  # Pour générer des identifiants uniques
from app.models.amenity import Amenity
from app.persistence.repository import AmenityRepository
from app.models.place import Place
from app.models.review import Review

# Simulation d'une base de données simple avec un dictionnaire
users_db = {}

# Instance du repository pour gérer le stockage des commodités
amenity_repo = AmenityRepository()

# Fonctions de gestion des utilisateurs (version simple)
def get_users():
    """Récupère tous les utilisateurs."""
    return list(users_db.values())

def get_user(user_id):
    """Récupère un utilisateur par son ID."""
    return users_db.get(user_id)

def create_user(data):
    """Crée un nouvel utilisateur."""
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
    """Met à jour un utilisateur existant."""
    if user_id not in users_db:
        return None
    
    user = users_db[user_id]
    user.update({
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email']
    })
    return user

def get_all_amenities():
    """Récupère toutes les commodités."""
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
    """
    Cette classe est le point d'entrée principal de l'application.
    
    Les dictionnaires (self.amenities, self.places, etc.) fonctionnent comme des mini-bases de données:
    - Les clés sont les ID uniques
    - Les valeurs sont les objets stockés
    
    Exemple:
    self.users = {
        'abc123': {'id': 'abc123', 'name': 'John', 'email': 'john@example.com'},
        'def456': {'id': 'def456', 'name': 'Jane', 'email': 'jane@example.com'}
    }
    """
    
    def __init__(self):
        """
        Initialisation des dictionnaires pour stocker les données.
        Chaque dictionnaire utilise les ID comme clés et les objets comme valeurs.
        """
        self.amenities = {}  # Stockage des commodités (ex: WiFi, Parking...)
        self.places = {}     # Stockage des lieux/logements
        self.users = {}      # Stockage des utilisateurs
        self.reviews = {}    # Stockage des avis

    def create_amenity(self, data):
        """
        Crée une nouvelle commodité.
        Args:
            data: dictionnaire contenant les données de la commodité (nom requis)
        Returns:
            tuple: (commodité créée, message d'erreur éventuel)
        """
        try:
            if 'name' not in data:
                return None, "Name is required"
            
            # Validation du nom avant création
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
        """
        La méthode .get() sur un dictionnaire est plus sûre que l'accès direct avec [].
        Exemple:
        - dict['clé'] lève une erreur si la clé n'existe pas
        - dict.get('clé', 'valeur_defaut') retourne 'valeur_defaut' si la clé n'existe pas
        
        Le try/except permet de gérer les erreurs gracieusement :
        - Si quelque chose échoue dans le try, le code continue dans le except
        - C'est comme avoir un plan B en cas d'erreur
        """
        try:
            # Configuration des valeurs par défaut pour les champs manquants 
            default_data = {
                'title': place_data.get('title', 'Unnamed Place'),
                'description': place_data.get('description', ''),
                'price': float(place_data.get('price', 0.0)),
                'latitude': float(place_data.get('latitude', 0.0)),
                'longitude': float(place_data.get('longitude', 0.0)),
                'owner_id': place_data.get('owner_id', 'default_owner'),
                'amenities': place_data.get('amenities', [])
            }

            place = Place(**default_data)  # ** décompresse le dictionnaire en arguments nommés
            self.places[place.id] = place
            return place.to_dict(), None
        except Exception:
            # En cas d'erreur, crée un lieu avec le minimum de données
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
        """
        Crée un nouvel utilisateur avec validation.
        Vérifie que tous les champs requis sont présents et que l'email est unique.
        """
        try:
            # Vérification des champs obligatoires
            required_fields = ['first_name', 'last_name', 'email']
            for field in required_fields:
                if field not in user_data:
                    return None, f"Missing required field: {field}"

            # Vérification de l'unicité de l'email
            for user in self.users.values():
                if user['email'] == user_data['email']:
                    return None, "Email already registered"

            # Création de l'utilisateur avec un ID unique
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

    def create_review(self, review_data):
        """
        Crée un nouvel avis.
        Utilise le modèle Review qui contient sa propre logique de validation.
        """
        try:
            review = Review(**review_data)
            self.reviews[review.id] = review
            return review.to_dict(), None
        except ValueError as e:
            return None, str(e)

    def get_review(self, review_id):
        """Get review by ID"""
        review = self.reviews.get(review_id)
        if not review:
            return None, "Review not found"
        return review.to_dict(), None

    def get_all_reviews(self):
        """Get all reviews"""
        return [review.to_dict() for review in self.reviews.values()]

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place"""
        if not self.places.get(place_id):
            return None, "Place not found"
        place_reviews = [review.to_dict() for review in self.reviews.values() 
                        if review.place_id == place_id]
        return place_reviews, None

    def update_review(self, review_id, review_data):
        """Update review"""
        review = self.reviews.get(review_id)
        if not review:
            return None, "Review not found"
        try:
            if 'rating' in review_data:
                Review.validate_rating(review_data['rating'])
                review.rating = review_data['rating']
            if 'text' in review_data:
                review.text = review_data['text']
            return review.to_dict(), None
        except ValueError as e:
            return None, str(e)

    def delete_review(self, review_id):
        """Delete review"""
        if review_id not in self.reviews:
            return "Review not found"
        del self.reviews[review_id]
        return None

def get_facade():
    """
    Fonction utilitaire qui retourne une instance de la façade.
    Permet d'avoir un point d'accès unique à la façade.
    """
    return HBnBFacade()
