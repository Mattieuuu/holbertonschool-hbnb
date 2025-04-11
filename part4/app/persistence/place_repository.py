# app/persistence/place_repository.py

from app.models.place import Place
from app import db
from sqlalchemy.exc import IntegrityError

class PlaceRepository:
    """Repository spécifique pour le modèle Place (sans relations)."""

    def __init__(self):
        self.model = Place

    def get_by_id(self, place_id):
        """Récupère un lieu (Place) par son ID."""
        return db.session.query(self.model).get(place_id)

    def create(self, title, description, price, latitude, longitude, owner_id=None):
        """Crée un nouveau lieu (Place) et l'enregistre en base."""
        try:
            place = self.model(
                title=title,
                description=description,
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner_id=owner_id,
            )
            db.session.add(place)
            db.session.commit()
            return place
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Erreur lors de la création du lieu (doublon ou contrainte invalide).")

    def update(self, place_id, data):
        """Met à jour les informations d'un lieu (Place)."""
        place = self.get_by_id(place_id)
        if not place:
            raise ValueError("Lieu introuvable.")

        # On ignore 'id' s'il est dans data, pour éviter des collisions
        for key, value in data.items():
            if hasattr(place, key) and key != "id":
                setattr(place, key, value)

        db.session.commit()
        return place

    def delete(self, place_id):
        """Supprime un lieu par son ID."""
        place = self.get_by_id(place_id)
        if not place:
            raise ValueError("Lieu introuvable.")

        db.session.delete(place)
        db.session.commit()
