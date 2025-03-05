from uuid import uuid4

class User:
    """Représente un utilisateur dans le système.
    
    Cette classe gère les informations des utilisateurs, notamment
    l'identification, les informations personnelles et les coordonnées.

    Attributs:
        id (str): Identifiant unique pour l'utilisateur
        email (str): Adresse email de l'utilisateur
        first_name (str): Prénom de l'utilisateur
        last_name (str): Nom de famille de l'utilisateur
    """
    def __init__(self, first_name, last_name, email, id=None):
        """Initialise une nouvelle instance d'Utilisateur.
        
        Args:
            first_name (str): Prénom de l'utilisateur
            last_name (str): Nom de famille de l'utilisateur
            email (str): Adresse email de l'utilisateur
            id (str, optionnel): Identifiant unique. Par défaut génère un UUID.
        """
        self.id = id or str(uuid4())
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        """Convertit l'instance utilisateur en représentation dictionnaire.
        
        Retourne:
            dict: Dictionnaire contenant les attributs de l'utilisateur
        """
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }