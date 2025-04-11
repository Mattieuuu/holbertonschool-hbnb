import unittest
from app.models.place import Place
from app.models.user import User

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.owner = User(first_name="John", last_name="Doe", email="john.doe@example.com")

    def test_valid_place(self):
        place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=self.owner)
        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.price, 100)
        self.assertEqual(place.latitude, 37.7749)
        self.assertEqual(place.longitude, -122.4194)

    def test_invalid_title(self):
        with self.assertRaises(ValueError):
            Place(title="", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=self.owner)

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", description="A nice place to stay", price=-100, latitude=37.7749, longitude=-122.4194, owner=self.owner)

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=100, longitude=-122.4194, owner=self.owner)

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-200, owner=self.owner)

if __name__ == '__main__':
    unittest.main()