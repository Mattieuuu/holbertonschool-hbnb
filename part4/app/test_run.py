import pytest
from app import create_app

# Fixtures pytest
# - Initialise une nouvelle instance de l'app pour chaque test
# - Assure l'isolation des tests
# - Facilite le partage de ressources entre les tests
@pytest.fixture
def app():
    """
    Fixture pytest qui crée une instance de test de l'application.
    Utilise la configuration de développement pour les tests.
    Returns:
        Flask: Instance de l'application configurée pour les tests.
    """
    return create_app("config.DevelopmentConfig")

# Tests unitaires
def test_app_creation(app):
    """
    Test de création de l'application.
    Vérifie:
    - Si l'application est créée correctement
    - Si le mode debug est activé
    - Si l'environnement est configuré en développement
    """
    assert app is not None
    assert app.config["DEBUG"] is True
    assert app.config["ENV"] == "development"
