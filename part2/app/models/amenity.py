"""
Les modèles (Models) sont des classes qui représentent les données de l'application.
Ils définissent la structure et les règles de validation des données.

C'est comme créer un moule pour faire des gâteaux :
- Le moule (la classe) définit la forme
- Chaque gâteau (instance) est unique mais a la même structure de base

Concepts Python utilisés ici :
- @property : Un décorateur qui permet d'accéder à une méthode comme si c'était un attribut
- @name.setter : Définit comment une propriété doit être modifiée
- raise ValueError : Permet d'arrêter l'exécution si une donnée est invalide

Par exemple:
class Person:
    @property
    def age(self):
        return self._age
        
    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("L'âge ne peut pas être négatif")
        self._age = value
"""

from .base_model import BaseModel

class Amenity(BaseModel):
    """Classe Commodité qui hérite de BaseModel"""
    
    def __init__(self, name=None):
        """Initialise une commodité"""
        super().__init__()
        self.name = name
        self.places = []

    def to_dict(self):
        """Convertit la commodité en dictionnaire"""
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict

    @staticmethod
    def validate_name(name: str):
        """Valide le nom de la commodité"""
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters")

    def add_place(self, place):
        """Ajoute un lieu à la commodité"""
        if place not in self.places:
            self.places.append(place)
            place.add_amenity(self)