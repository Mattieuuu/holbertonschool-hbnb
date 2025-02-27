import re
from datetime import datetime
from .base_model import BaseModel

# Pour gérer de manière globale les emails déjà utilisés
# (Uniquement à des fins d’exemple si on veut imposer l’unicité en mémoire)
USED_EMAILS = set()

def is_valid_email(email: str) -> bool:
    """
    Vérifie si l'email suit un format basique.
    """
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(pattern, email) is not None

class User(BaseModel):
    """
    Représentation d'un utilisateur (User).
    """
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        is_admin: bool = False,
        *args, **kwargs
    ):
        """
        Initialise l’objet User avec les attributs requis et par défaut.
        """
        super().__init__(*args, **kwargs)

        # Vérifications et affectations
        # 1. Longueur max 50 chars pour first_name / last_name
        if len(first_name) > 50:
            raise ValueError("first_name must not exceed 50 characters.")
        if len(last_name) > 50:
            raise ValueError("last_name must not exceed 50 characters.")

        # 2. Email valide et unique
        if not is_valid_email(email):
            raise ValueError("Email format is invalid.")
        if email in USED_EMAILS:
            raise ValueError("Email must be unique. This email is already used.")
        USED_EMAILS.add(email)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def update(self, data: dict):
        """
        Surcharge pour gérer les règles spécifiques à User lors de la mise à jour.
        """
        # On vérifie par exemple si l'email change et reste unique
        if "email" in data:
            new_email = data["email"]
            if not is_valid_email(new_email):
                raise ValueError("Email format is invalid.")
            if new_email != self.email and new_email in USED_EMAILS:
                raise ValueError("Email must be unique. This email is already used.")
            # On retire l'ancien email du set et on ajoute le nouveau si besoin
            USED_EMAILS.discard(self.email)
            USED_EMAILS.add(new_email)

        # Vérification de la longueur first_name, last_name
        if "first_name" in data and len(data["first_name"]) > 50:
            raise ValueError("first_name must not exceed 50 characters.")
        if "last_name" in data and len(data["last_name"]) > 50:
            raise ValueError("last_name must not exceed 50 characters.")

        super().update(data)  # Appel du update() de BaseModel
