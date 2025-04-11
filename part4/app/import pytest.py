import pytest
from app import create_app

@pytest.fixture
def app():
    return create_app("config.DevelopmentConfig")

def test_app_creation(app):
    assert app is not None
    assert app.config["DEBUG"] is True
    assert app.config["ENV"] == "development"  # ✅ Corrigé : aligné et pas en double
