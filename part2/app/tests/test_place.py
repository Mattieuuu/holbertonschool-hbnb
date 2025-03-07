import unittest
from models.place import Place
from models.base_model import BaseModel

class TestPlace(unittest.TestCase):
    def test_place_creation(self):
        place = Place("Maison de vacances", "Belle maison près de la plage", 100.0, 43.5, 7.0, "owner123", ["wifi", "piscine"])
        self.assertIsInstance(place, Place)
        self.assertIsInstance(place, BaseModel)
        self.assertEqual(place.title, "Maison de vacances")
        self.assertEqual(place.description, "Belle maison près de la plage")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 43.5)
        self.assertEqual(place.longitude, 7.0)
        self.assertEqual(place.owner_id, "owner123")
        self.assertEqual(place.amenities, ["wifi", "piscine"])

    def test_place_creation_default_values(self):
        place = Place()
        self.assertEqual(place.title, "Lieu sans nom")
        self.assertEqual(place.description, "")
        self.assertEqual(place.price, 0.0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertEqual(place.owner_id, "default_owner")
        self.assertEqual(place.amenities, [])

    def test_safe_float(self):
        self.assertEqual(Place._safe_float("10.5", 0.0), 10.5)
        self.assertEqual(Place._safe_float("not a number", 0.0), 0.0)

    def test_validate_valid_data(self):
        place = Place("Valid Title", "Description", 50.0, 45.0, 90.0)
        place.validate()  # Should not raise any exception

    def test_validate_invalid_data(self):
        with self.assertRaises(ValueError):
            Place("" * 101).validate()  # Title too long
        with self.assertRaises(ValueError):
            Place(price=-10).validate()  # Negative price
        with self.assertRaises(ValueError):
            Place(latitude=91).validate()  # Invalid latitude
        with self.assertRaises(ValueError):
            Place(longitude=181).validate()  # Invalid longitude

    def test_add_amenity(self):
        place = Place()
        place.add_amenity("wifi")
        place.add_amenity("parking")
        place.add_amenity("wifi")  # Adding duplicate
        self.assertEqual(place.amenities, ["wifi", "parking"])

    def test_to_dict(self):
        place = Place("Test Place", "Test Description", 75.5, 40.0, -74.0, "owner456", ["gym"])
        place_dict = place.to_dict()
        self.assertIsInstance(place_dict, dict)
        self.assertEqual(place_dict['title'], "Test Place")
        self.assertEqual(place_dict['description'], "Test Description")
        self.assertEqual(place_dict['price'], 75.5)
        self.assertEqual(place_dict['latitude'], 40.0)
        self.assertEqual(place_dict['longitude'], -74.0)
        self.assertEqual(place_dict['owner_id'], "owner456")
        self.assertEqual(place_dict['amenities'], ["gym"])
        self.assertIn('id', place_dict)
        self.assertIn('created_at', place_dict)
        self.assertIn('updated_at', place_dict)

if __name__ == '__main__':
    unittest.main()