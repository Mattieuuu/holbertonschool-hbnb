# app/models/amenity.py

from app import db
from .base_model import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .place import place_amenity_association  # ✅ Ajout de l'import

class Amenity(BaseModel, db.Model):
    """
    Modèle Amenity en SQLAlchemy, lié à Place par une relation Many-to-Many.
    """
    __tablename__ = 'amenities'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # ✅ Relation Many-to-Many avec Place
    places = relationship('Place', secondary='place_amenity_association', back_populates='amenities', lazy=True)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name must be a non-empty string")
        if len(self.name) > 50:
            raise ValueError("Name must be 50 characters or less")

    def __repr__(self):
        return f"<Amenity name='{self.name}'>"