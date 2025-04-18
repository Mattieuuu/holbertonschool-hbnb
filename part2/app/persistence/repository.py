"""
Le Repository Pattern est un concept qui isole le code qui accède aux données.

Imaginez une bibliothèque :
- Les livres sont rangés quelque part (base de données)
- Le bibliothécaire (repository) sait exactement où trouver chaque livre
- Les visiteurs (le reste du code) demandent simplement un livre au bibliothécaire

Avantages :
1. On peut changer la façon dont les données sont stockées sans modifier le reste du code
2. La logique de stockage est centralisée à un seul endroit
3. Le code est plus facile à tester

Dans ce fichier :
- Les méthodes CRUD (Create, Read, Update, Delete) sont les opérations de base
- Le stockage utilise un dictionnaire, mais pourrait facilement être changé pour une vraie base de données
"""

from abc import ABC, abstractmethod
from app.models.amenity import Amenity

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

# -------------------- Repository spécifique pour les commodités --------------------
class AmenityRepository(InMemoryRepository):
    def __init__(self):
        super().__init__()

    def add(self, amenity):
        """Ajoute une commodité dans le stockage"""
        if not isinstance(amenity, Amenity):
            raise ValueError("L'objet doit être une instance de Amenity")
        super().add(amenity)

    def get(self, amenity_id):
        """Récupère une commodité par son ID"""
        return super().get(amenity_id)

    def get_all(self):
        """Récupère toutes les commodités"""
        return super().get_all()

    def update(self, amenity_id, data):
        """Met à jour une commodité"""
        super().update(amenity_id, data)

    def delete(self, amenity_id):
        """Supprime une commodité par son ID"""
        super().delete(amenity_id)

    def get_by_attribute(self, attr_name, attr_value):
        """Recherche une commodité par un attribut spécifique"""
        return super().get_by_attribute(attr_name, attr_value)