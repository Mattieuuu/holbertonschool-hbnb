from app import db
from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.user import User



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
    amenities = relationship('Amenity', secondary=place_amenity_association, back_populates='places', lazy=True)

    def __init__(self, title, description="", price=0.0, latitude=0.0, longitude=0.0, owner_id=None, owner=None):
        super().__init__()
        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        self.owner_id = owner_id
        if owner:
            self.owner = owner
            self.owner_id = owner.id

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
            raise ValueError("Latitude must be a number between -90 and 90")
        if not isinstance(self.longitude, (int, float)) or not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be a number between -180 and 180")

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def __repr__(self):
        return f"<Place id={self.id} title={self.title}>"
