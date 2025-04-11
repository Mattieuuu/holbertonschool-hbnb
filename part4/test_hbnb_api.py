import unittest
import requests

# Définition de l'URL de base (assurez-vous que votre API est lancée sur localhost:5000)
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
PLACES_URL = f"{BASE_URL}/places"

# Utilisateur de test (doit exister dans la base de données, sinon ajustez)
TEST_USER = {
    "email": "admin@hbnb.com",
    "password": "admin123"
}

class TestHBNBAPI(unittest.TestCase):
    def setUp(self):
        """Récupère un token JWT valide pour les tests authentifiés."""
        response = requests.post(LOGIN_URL, json=TEST_USER)
        self.assertEqual(response.status_code, 200, "La connexion a échoué lors du setup")
        data = response.json()
        self.token = data.get("access_token")
        self.auth_headers = {"Authorization": f"Bearer {self.token}"}

    def test_valid_login(self):
        """Teste la connexion avec des identifiants valides."""
        response = requests.post(LOGIN_URL, json=TEST_USER)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data, "Le token n'est pas présent dans la réponse de login")

    def test_invalid_login(self):
        """Teste la connexion avec de mauvais identifiants."""
        bad_credentials = {"email": "admin@hbnb.com", "password": "wrongpass"}
        response = requests.post(LOGIN_URL, json=bad_credentials)
        # Selon l’implémentation, on peut obtenir 400 ou 401
        self.assertIn(response.status_code, [400, 401], "Le code retourné pour une connexion invalide n'est ni 400 ni 401")

    def test_get_places_authenticated(self):
        """Teste l'accès à la liste des lieux avec authentification."""
        response = requests.get(PLACES_URL + "/", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200, "L'accès aux lieux authentifiés a échoué")
        places = response.json()
        self.assertIsInstance(places, list, "La réponse n'est pas une liste")
        # Si aucun lieu n'est retourné, le test passe tout de même (mais on pourra créer des données si besoin)

    def test_get_places_unauthenticated(self):
        """Teste l'accès à la liste des lieux sans authentification."""
        response = requests.get(PLACES_URL + "/")
        # Selon l’implémentation, l'accès non authentifié devrait être refusé
        self.assertNotEqual(response.status_code, 200, "L'accès non authentifié ne doit pas renvoyer 200")

    def test_get_place_details_authenticated(self):
        """Teste l'accès aux détails d'un lieu en passant par l'API avec authentification."""
        # Récupère d'abord la liste des lieux
        places_response = requests.get(PLACES_URL + "/", headers=self.auth_headers)
        self.assertEqual(places_response.status_code, 200, "La récupération des lieux a échoué")
        places = places_response.json()
        if not places:
            self.skipTest("Aucun lieu disponible pour tester les détails")
        # Utilise le premier lieu pour récupérer ses détails
        place_id = places[0]["id"]
        detail_response = requests.get(f"{PLACES_URL}/{place_id}", headers=self.auth_headers)
        self.assertEqual(detail_response.status_code, 200, "L'accès aux détails du lieu a échoué")
        place_detail = detail_response.json()
        # Vérifie la présence de certaines clés essentielles
        for key in ["title", "description", "reviews", "amenities"]:
            self.assertIn(key, place_detail, f"La clé '{key}' est absente dans les détails du lieu")

    def test_get_place_details_unauthenticated(self):
        """Teste l'accès aux détails d'un lieu sans authentification."""
        # Récupère d'abord la liste des lieux authentifiée
        places_response = requests.get(PLACES_URL + "/", headers=self.auth_headers)
        self.assertEqual(places_response.status_code, 200)
        places = places_response.json()
        if not places:
            self.skipTest("Aucun lieu disponible pour tester les détails")
        place_id = places[0]["id"]
        detail_response = requests.get(f"{PLACES_URL}/{place_id}")
        # Le résultat attendu pour une requête non authentifiée peut être un code 401 ou 403
        self.assertIn(detail_response.status_code, [401, 403],
                      "L'accès non authentifié aux détails du lieu devrait renvoyer 401 ou 403")

    def test_reviews_structure_in_place_detail(self):
        """Vérifie que la structure des reviews dans les détails d'un lieu est conforme."""
        headers = self.auth_headers
        places_response = requests.get(PLACES_URL + "/", headers=headers)
        self.assertEqual(places_response.status_code, 200)
        places = places_response.json()
        if not places:
            self.skipTest("Aucun lieu disponible pour tester les reviews")
        place_id = places[0]["id"]
        detail_response = requests.get(f"{PLACES_URL}/{place_id}", headers=headers)
        self.assertEqual(detail_response.status_code, 200)
        place_detail = detail_response.json()
        self.assertIn("reviews", place_detail)
        reviews = place_detail["reviews"]
        self.assertIsInstance(reviews, list)
        # Pour chaque review, vérifier les clés attendues
        for review in reviews:
            self.assertIn("rating", review)
            self.assertIn("text", review)
            self.assertIn("user", review)
            self.assertIsInstance(review["user"], dict)
            self.assertIn("first_name", review["user"])

    def test_token_in_cookie_simulation(self):
        """Test basique pour s'assurer que le token obtenu n'est pas vide."""
        self.assertIsNotNone(self.token, "Le token est None")
        self.assertNotEqual(self.token.strip(), "", "Le token est une chaîne vide")

if __name__ == '__main__':
    unittest.main()
