import unittest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

class TestReview(unittest.TestCase):
    def setUp(self):
        self.user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=self.user)

    def test_valid_review(self):
        review = Review(text="Great place!", rating=5, place=self.place, user=self.user)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)

    def test_invalid_text(self):
        with self.assertRaises(ValueError):
            Review(text="", rating=5, place=self.place, user=self.user)

    def test_invalid_rating(self):
        with self.assertRaises(ValueError):
            Review(text="Great place!", rating=6, place=self.place, user=self.user)

    def test_invalid_place(self):
        with self.assertRaises(ValueError):
            Review(text="Great place!", rating=5, place=None, user=self.user)

    def test_invalid_user(self):
        with self.assertRaises(ValueError):
            Review(text="Great place!", rating=5, place=self.place, user=None)

if __name__ == '__main__':
    unittest.main()