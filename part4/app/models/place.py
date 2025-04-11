from app import db
from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# 👇 on définit l'association ici, comme demandé par ton école
place_amenity_association = Table(
    'place_amenity_association',
    db.metadata,
    Column('place_id', Integer, ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel, db.Model):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, default=0.0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='places', lazy=True)

    reviews = relationship('Review', back_populates='place', lazy=True)

    # Utilisation d'une string dans relationship() pour éviter les imports circulaires
    amenities = relationship('Amenity', secondary=place_amenity_association, back_populates='places', lazy=True)

    def __init__(self, title, description="", price=0.0, latitude=0.0, longitude=0.0, owner_id=None, owner=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        # Gestion de owner et owner_id :
        if owner and owner_id:
            if int(owner_id) != owner.id:
                raise ValueError("owner_id does not match owner.id")
            self.owner = owner
            self.owner_id = owner.id
        elif owner:
            self.owner = owner
            self.owner_id = owner.id
        elif owner_id:
            self.owner_id = int(owner_id)
        else:
            raise ValueError("owner or owner_id must be provided")

        self.reviews = []
        self.amenities = []

        self.validate_attributes()

    def validate_attributes(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a non-negative number")
        if not isinstance(self.latitude, (int, float)) or not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not isinstance(self.longitude, (int, float)) or not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def __repr__(self):
        return f"<Place id={self.id} title={self.title}>"
