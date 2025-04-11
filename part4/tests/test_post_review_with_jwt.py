import pytest
from flask import json
from app import create_app, db
from app.models import User, Place

@pytest.fixture
def client():
    app = create_app("config.TestingConfig")  # ou DevelopmentConfig si tu préfères
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Créer un utilisateur
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            db.session.add(user)

            # Créer un lieu
            place = Place(
                name="Test Place",
                description="Test description",
                city="Paris",
                country="France",
                price_per_night=100,
                max_guests=2,
                owner=user
            )
            db.session.add(place)
            db.session.commit()

        yield client

        with app.app_context():
            db.drop_all()

def get_token(client):
    """Connexion et récupération du token JWT"""
    login_data = {
        "email": "john@example.com",
        "password": "password123"
    }
    res = client.post("/api/v1/auth/login", json=login_data)
    token = res.json.get("access_token")
    return token

def test_post_review_with_jwt(client):
    """Test POST /reviews avec JWT"""
    token = get_token(client)

    # Récupérer l'ID du lieu
    place_id = Place.query.first().id

    review_data = {
        "text": "Super endroit !",
        "rating": 5,
        "place_id": place_id
    }

    res = client.post(
        "/api/v1/reviews",
        json=review_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 201
    assert "id" in res.json
    assert res.json["text"] == "Super endroit !"
