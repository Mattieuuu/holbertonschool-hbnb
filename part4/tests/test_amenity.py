import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    def test_valid_amenity(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            Amenity(name="")

    def test_name_too_long(self):
        with self.assertRaises(ValueError):
            Amenity(name="A" * 51)

if __name__ == '__main__':
    unittest.main()