import logging
from abc import ABC, abstractmethod
from app.extensions import db  # Import SQLAlchemy instance for database operations

logger = logging.getLogger(__name__)


class Repository(ABC):
    """Abstract base class for repositories."""

    @abstractmethod
    def add(self, obj):
        """Add an object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects in the repository."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object by its ID with new data."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute."""
        pass


class InMemoryRepository(Repository):
    """In-memory implementation of the repository for testing and prototyping."""

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        logger.debug(f"Adding item with ID {obj.id} to repository")
        self._storage[obj.id] = obj
        logger.debug(f"Repository now contains {len(self._storage)} items")
        return obj

    def get(self, obj_id):
        logger.debug(f"Fetching item with ID {obj_id}")
        obj = self._storage.get(obj_id)
        if obj:
            logger.debug(f"Found item with ID {obj_id}")
        else:
            logger.debug(f"No item found with ID {obj_id}")
        return obj

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        if obj_id in self._storage:
            obj = self._storage[obj_id]
            for key, value in data.items():
                setattr(obj, key, value)
            logger.debug(f"Updated item with ID {obj_id}")
            return obj
        logger.debug(f"Failed to update: no item with ID {obj_id}")
        return None

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            logger.debug(f"Deleted item with ID {obj_id}")
            return True
        logger.debug(f"Failed to delete: no item with ID {obj_id}")
        return False

    def get_by_attribute(self, attr_name, attr_value):
        logger.debug(f"Searching for item with {attr_name}={attr_value}")
        for obj in self._storage.values():
            if getattr(obj, attr_name, None) == attr_value:
                logger.debug(f"Found item with {attr_name}={attr_value}")
                return obj
        logger.debug(f"No item found with {attr_name}={attr_value}")
        return None


class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of the repository for persistent storage."""

    def __init__(self, model):
        """
        Initialize the repository with a specific SQLAlchemy model.

        :param model: The SQLAlchemy model class this repository manages.
        """
        self.model = model

    def add(self, obj):
        """
        Add a new object to the database.

        :param obj: The object to be added.
        :return: The added object.
        """
        logger.debug(f"Adding item with ID {getattr(obj, 'id', None)} to repository")
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """
        Fetch an object by its ID.

        :param obj_id: The ID of the object to fetch.
        :return: The fetched object or None if not found.
        """
        logger.debug(f"Fetching item with ID {obj_id}")
        return self.model.query.get(obj_id)

    def get_all(self):
        """
        Fetch all objects of this model.

        :return: A list of all objects.
        """
        logger.debug("Fetching all items from repository")
        return self.model.query.all()

    def update(self, obj_id, data):
        """
        Update an existing object by its ID.

        :param obj_id: The ID of the object to update.
        :param data: A dictionary of attributes to update.
        :return: The updated object or None if not found.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            logger.debug(f"Updated item with ID {obj_id}")
            return obj
        logger.debug(f"Failed to update: no item with ID {obj_id}")
        return None

    def delete(self, obj_id):
        """
        Delete an object by its ID.

        :param obj_id: The ID of the object to delete.
        :return: True if deleted successfully, False otherwise.
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            logger.debug(f"Deleted item with ID {obj_id}")
            return True
        logger.debug(f"Failed to delete: no item with ID {obj_id}")
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """
        Fetch an object by a specific attribute.

        :param attr_name: The name of the attribute to filter by.
        :param attr_value: The value of the attribute to filter by.
        :return: The first matching object or None if not found.
        """
        logger.debug(f"Searching for item with {attr_name}={attr_value}")
        # Use getattr to access the attribute of the model and filter by it
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()
