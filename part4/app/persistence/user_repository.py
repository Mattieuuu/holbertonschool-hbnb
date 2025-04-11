from app.models.user import User
from app import db
from sqlalchemy.exc import IntegrityError

class UserRepository:
    """Repository spécifique pour le modèle User."""

    def __init__(self):
        self.model = User

    def get_by_id(self, user_id):
        """Récupère un utilisateur par son ID."""
        return db.session.query(self.model).get(user_id)

    def get_by_email(self, email):
        """Récupère un utilisateur par son email."""
        return db.session.query(self.model).filter_by(email=email).first()

    def create(self, first_name, last_name, email, password, is_admin=False):
        """Crée un nouvel utilisateur."""
        try:
            user = self.model(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_admin=is_admin,
            )
            user.hash_password(password)  # Hashage du mot de passe
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Email déjà utilisé.")

    def update(self, user_id, data):
        """Met à jour les informations d'un utilisateur."""
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")

        for key, value in data.items():
            if hasattr(user, key) and key != "id":
                setattr(user, key, value)

        db.session.commit()
        return user

    def delete(self, user_id):
        """Supprime un utilisateur par son ID."""
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")

        db.session.delete(user)
        db.session.commit()

    def get_all(self):
        """Retourne la liste de tous les utilisateurs."""
        return db.session.query(self.model).all()
