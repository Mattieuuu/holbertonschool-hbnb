from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Name must be a non-empty string")
        if len(self.name) > 50:
            raise ValueError("Name must be 50 characters or less")