# models/review.py
from .base_model import BaseModel

class Review(BaseModel):
    """Review class for storing place reviews"""
    def __init__(self, text, rating, user_id, place_id):
        """Initialize review"""
        super().__init__()
        self.validate_rating(rating)
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    @staticmethod
    def validate_rating(rating):
        """Validate rating is between 1 and 5"""
        try:
            rating = int(rating)
            if not 1 <= rating <= 5:
                raise ValueError("Rating must be between 1 and 5")
        except (TypeError, ValueError):
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        """Convert review to dictionary"""
        review_dict = super().to_dict()
        review_dict.update({
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        return review_dict