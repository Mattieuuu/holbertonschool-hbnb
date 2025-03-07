import unittest
from models.amenity import Amenity
from models.base_model import BaseModel

class TestAmenity(unittest.TestCase):
    def test_amenity_creation(self):
        amenity = Amenity("Piscine")
        self.assertIsInstance(amenity, Amenity)
        self.assertIsInstance(amenity, BaseModel)
        self.assertEqual(amenity.name, "Piscine")
        self.assertEqual(amenity.places, [])

    def test_amenity_default_name(self):
        amenity = Amenity()
        self.assertIsNone(amenity.name)
        self.assertEqual(amenity.places, [])

    def test_to_dict(self):
        amenity = Amenity("WiFi")
        amenity_dict = amenity.to_dict()
        self.assertIsInstance(amenity_dict, dict)
        self.assertEqual(amenity_dict['name'], "WiFi")
        self.assertIn('id', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)

    def test_validate_name_valid(self):
        Amenity.validate_name("Parking")
        Amenity.validate_name("Salle de sport")  # Pas d'exception levée = valide

    def test_validate_name_invalid(self):
        with self.assertRaises(ValueError):
            Amenity.validate_name("")  # Nom vide
        with self.assertRaises(ValueError):
            Amenity.validate_name("A" * 51)  # Nom trop long

    def test_add_place(self):
        class MockPlace:
            """Classe simulée pour tester l'ajout de commodités"""
            def __init__(self):
                self.amenities = []

            def add_amenity(self, amenity):
                if amenity not in self.amenities:
                    self.amenities.append(amenity)

        place = MockPlace()
        amenity = Amenity("Terrasse")
        
        # Ajout d'un lieu à la commodité
        amenity.add_place(place)
        self.assertIn(place, amenity.places)
        
        # Vérifie que la commodité est ajoutée au lieu
        self.assertIn(amenity, place.amenities)

if __name__ == '__main__':
    unittest.main()