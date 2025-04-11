import os

# Obtention du chemin absolu du répertoire courant
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clé secrète utilisée pour la sécurité de l'application
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = SECRET_KEY
    
    # Configuration de la base de données SQLite
    # Le fichier sera créé dans le dossier 'instance'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    
    # Désactive le suivi des modifications de SQLAlchemy
    # pour améliorer les performances
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    # Active le mode debug pour l'environnement de développement
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'development.db')}"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'development.db')}"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'development.db')}"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
