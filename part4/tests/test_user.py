import unittest
from app.models.user import User

class TestUser(unittest.TestCase):
    def test_valid_user(self):
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")

    def test_invalid_first_name(self):
        with self.assertRaises(ValueError):
            User(first_name="", last_name="Doe", email="john.doe@example.com")

    def test_invalid_last_name(self):
        with self.assertRaises(ValueError):
            User(first_name="John", last_name="", email="john.doe@example.com")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User(first_name="John", last_name="Doe", email="invalid-email")

if __name__ == '__main__':
    unittest.main()