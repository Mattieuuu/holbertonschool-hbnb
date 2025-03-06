import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models"""
    
    def __init__(self):
        """Initialize base model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update updated_at timestamp"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Convert model to dictionary"""
        result = self.__dict__.copy()
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        result['__class__'] = self.__class__.__name__
        return result

    @classmethod
    def from_dict(cls, data):
        """Create instance from dictionary"""
        instance = cls()
        for key, value in data.items():
            if key not in ['__class__', 'created_at', 'updated_at']:
                setattr(instance, key, value)
        return instance