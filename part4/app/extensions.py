# Module de configuration des extensions Flask
# 
# Objectif architectural:
# - Centraliser la configuration des extensions
# - Permettre une initialisation lazy des extensions
# - Faciliter les tests unitaires
# 
# Utilisation dans l'application:
# - Les extensions sont importées dans les autres modules
# - L'initialisation finale se fait dans create_app()
# - Chaque extension peut être mockée pour les tests

# Ce fichier est crucial pour:
# - La séparation des préoccupations
# - L'évitement des imports circulaires
# - La réutilisation des extensions dans différentes parties de l'application

# Structure du fichier:
# 1. Imports des extensions Flask
# 2. Initialisation des instances
# 3. Configuration des comportements par défaut

# Les extensions utilisées:
# - SQLAlchemy: Gestion de la base de données
# - Bcrypt: Sécurité des mots de passe
# - JWTManager: Authentification par tokens

# Imports des extensions nécessaires
# SQLAlchemy : ORM pour la gestion de la base de données relationnelle
# Bcrypt : Bibliothèque pour le hachage sécurisé des mots de passe
# JWTManager : Gestionnaire des tokens JWT pour l'authentification
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialisation des instances
# Chaque instance est créée sans paramètres
# La configuration sera faite dans create_app()

# JWTManager : Gère l'authentification par tokens
jwt = JWTManager()

# SQLAlchemy : Interface avec la base de données
# Permet la création de modèles et la gestion des requêtes
db = SQLAlchemy()

# Bcrypt : Sécurisation des mots de passe
# Fournit des fonctions de hachage et de vérification
bcrypt = Bcrypt()
