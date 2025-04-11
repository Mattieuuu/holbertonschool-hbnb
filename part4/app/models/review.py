from app import db
from .base_model import BaseModel
from .place import Place
from .user import User
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    place = relationship("Place", back_populates="reviews", lazy=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="reviews", lazy=True)

    def __init__(self, text, rating, place=None, user=None):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.validate_attributes()

    def validate_attributes(self):
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("Text must be a non-empty string")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not self.place:
            raise ValueError("Review must be associated with a valid Place")
        if not isinstance(self.place, Place):
            raise ValueError("place must be an instance of Place")
        if not self.user:
            raise ValueError("Review must be associated with a valid User")
        if not isinstance(self.user, User):
            raise ValueError("user must be an instance of User")

    def __repr__(self):
        return f"<Review id={self.id} rating={self.rating}>"
