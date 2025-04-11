from app import db  # Obligatoire pour que SQLAlchemy fonctionne

# On importe d’abord les dépendances de base pour éviter les boucles
from .base_model import BaseModel

# Puis les autres modèles
from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity
