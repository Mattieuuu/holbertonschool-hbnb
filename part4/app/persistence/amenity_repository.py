# app/persistence/amenity_repository.py

from app.models.amenity import Amenity
from app import db
from sqlalchemy.exc import IntegrityError

class AmenityRepository:
    """
    Repository spécifique pour le modèle Amenity,
    sans relation ni ForeignKey.
    """

    def __init__(self):
        self.model = Amenity

    def get_by_id(self, amenity_id):
        """Récupère un aménagement (Amenity) par son ID."""
        return db.session.query(self.model).get(amenity_id)

    def create(self, name):
        """Crée un nouvel aménagement (Amenity) et l'enregistre en base."""
        try:
            amenity = self.model(name=name)
            db.session.add(amenity)
            db.session.commit()
            return amenity
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Erreur lors de la création de l'amenity (contrainte invalide).")

    def update(self, amenity_id, data):
        """Met à jour les informations d'un aménagement (Amenity)."""
        amenity = self.get_by_id(amenity_id)
        if not amenity:
            raise ValueError("Amenity introuvable.")

        for key, value in data.items():
            if hasattr(amenity, key) and key != "id":
                setattr(amenity, key, value)

        db.session.commit()
        return amenity

    def delete(self, amenity_id):
        """Supprime un aménagement (Amenity) par son ID."""
        amenity = self.get_by_id(amenity_id)
        if not amenity:
            raise ValueError("Amenity introuvable.")

        db.session.delete(amenity)
        db.session.commit()
