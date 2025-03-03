# models/place.py
from .base_model import BaseModel

class Place(BaseModel):
    """Class representing a place"""

    def __init__(self, title="Unnamed Place", description="", price=0.0, 
                 latitude=0.0, longitude=0.0, owner_id=None, amenities=None):
        """Initialize place with safe defaults"""
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
        """Convert value to float safely"""
        try:
            result = float(value)
            return result
        except (TypeError, ValueError):
            return default

    def validate(self):
        """Validate place data"""
        if not self.title or len(self.title) > 100:
            raise ValueError("Title must be between 1 and 100 characters")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not -90 <= self.latitude <= 90:
            raise ValueError("Invalid latitude")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Invalid longitude")

    def add_amenity(self, amenity_id):
        """Add amenity to place"""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def to_dict(self):
        """Convert place to dictionary"""
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