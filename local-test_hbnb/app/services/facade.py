from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

# services/facade.py
class HBnBFacade:
    
    def __init__(self):
        self.amenity_repo = InMemoryRepository()  # Stockage en mémoire pour les équipements

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)  # Création d'un objet Amenity à partir des données
        self.amenity_repo.add(amenity)  # Ajouter l'équipement au repository
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)  # Récupérer un équipement par ID

    def get_all_amenities(self):
        return self.amenity_repo.get_all()  # Récupérer tous les équipements

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)  # Mettre à jour l'équipement avec les nouvelles données
            self.amenity_repo.update(amenity)  # Sauvegarder l'équipement mis à jour
        return amenity
