from .base_model import BaseModel

class Amenity(BaseModel):
    """Amenity class that inherits from BaseModel"""
    
    def __init__(self, name=None):
        """Initialize amenity"""
        super().__init__()
        self.name = name
        self.places = []

    def to_dict(self):
        """Convert amenity to dictionary"""
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict

    @staticmethod
    def validate_name(name: str):
        """Validate amenity name"""
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters")

    def add_place(self, place):
        """Add a place to the amenity"""
        if place not in self.places:
            self.places.append(place)
            place.add_amenity(self)