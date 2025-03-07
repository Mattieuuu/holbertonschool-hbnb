import unittest
from uuid import UUID
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models')))
from user import User

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User("John", "Doe", "john.doe@example.com")
        self.assertIsInstance(user, User)
        self.assertIsInstance(UUID(user.id), UUID)
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_user_creation_with_id(self):
        user_id = "12345678-1234-5678-1234-567812345678"
        user = User("Jane", "Smith", "jane.smith@example.com", id=user_id)
        self.assertEqual(user.id, user_id)

    def test_to_dict(self):
        user = User("Alice", "Johnson", "alice.johnson@example.com")
        user_dict = user.to_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['email'], "alice.johnson@example.com")
        self.assertEqual(user_dict['first_name'], "Alice")
        self.assertEqual(user_dict['last_name'], "Johnson")
        self.assertIn('id', user_dict)

if __name__ == '__main__':
    unittest.main()