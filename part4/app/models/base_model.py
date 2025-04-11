# app/models/base_model.py
import uuid
from datetime import datetime
from app import db  # Import de SQLAlchemy pour que BaseModel soit un modèle ORM
from sqlalchemy import Column, String, DateTime

class BaseModel(db.Model):
    __abstract__ = True  # Indique que cette classe ne doit pas créer de table

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
