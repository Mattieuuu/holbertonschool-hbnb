"""
La classe Place représente un logement ou un lieu dans l'application.

Points importants en Python :
1. Initialisation avec __init__ :
   - C'est comme préparer une nouvelle maison avant que quelqu'un y emménage
   - self fait référence à l'instance spécifique qu'on crée

2. Méthode to_dict :
   - Convertit l'objet en dictionnaire pour le stockage ou l'API
   - C'est comme prendre une photo de l'état actuel de l'objet

3. Validation des données :
   - Vérifie que les données sont correctes (prix positif, coordonnées valides, etc.)
   - C'est comme un agent immobilier qui vérifie que tout est en ordre

4. Types de données en Python :
   - float : nombres décimaux (prix, latitude, longitude)
   - str : texte (titre, description)
   - list : collection ordonnée (liste des commodités)
"""

# models/place.py
from .base_model import BaseModel

class Place(BaseModel):
    """Classe représentant un lieu"""

    def __init__(self, title="Lieu sans nom", description="", price=0.0, 
                 latitude=0.0, longitude=0.0, owner_id=None, amenities=None):
        """Initialise un lieu avec des valeurs par défaut sécurisées"""
        super().__init__()
        self.title = str(title)
        self.description = str(description) if description else ""
        self.price = self._safe_float(price, 0.0)
        self.latitude = self._safe_float(latitude, 0.0)
        self.longitude = self._safe_float(longitude, 0.0)
        self.owner_id = owner_id if owner_id else "default_owner"
        self.amenities = list(amenities) if amenities else []

    @staticmethod
    def _safe_float(value, default):
        """Convertit une valeur en float de manière sécurisée"""
        try:
            result = float(value)
            return result
        except (TypeError, ValueError):
            return default

    def validate(self):
        """Valide les données du lieu"""
        if not self.title or len(self.title) > 100:
            raise ValueError("Title must be between 1 and 100 characters")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not -90 <= self.latitude <= 90:
            raise ValueError("Invalid latitude")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Invalid longitude")

    def add_amenity(self, amenity_id):
        """Ajoute une commodité au lieu"""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def to_dict(self):
        """Convertit le lieu en dictionnaire"""
        place_dict = super().to_dict()
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': self.amenities
        })
        return place_dict