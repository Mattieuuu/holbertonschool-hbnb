import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models')))
from review import Review
from base_model import BaseModel

class TestReview(unittest.TestCase):
    def test_review_creation(self):
        review = Review("Great place!", 5, "user123", "place456")
        self.assertIsInstance(review, Review)
        self.assertIsInstance(review, BaseModel)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user_id, "user123")
        self.assertEqual(review.place_id, "place456")

    def test_validate_rating_valid(self):
        Review.validate_rating(1)
        Review.validate_rating(3)
        Review.validate_rating(5)
        # Si aucune exception n'est levée, le test passe

    def test_validate_rating_invalid(self):
        with self.assertRaises(ValueError):
            Review.validate_rating(0)
        with self.assertRaises(ValueError):
            Review.validate_rating(6)
        with self.assertRaises(ValueError):
            Review.validate_rating("not a number")

    def test_to_dict(self):
        review = Review("Nice view", 4, "user789", "place101")
        review_dict = review.to_dict()
        self.assertIsInstance(review_dict, dict)
        self.assertEqual(review_dict['text'], "Nice view")
        self.assertEqual(review_dict['rating'], 4)
        self.assertEqual(review_dict['user_id'], "user789")
        self.assertEqual(review_dict['place_id'], "place101")
        self.assertIn('id', review_dict)
        self.assertIn('created_at', review_dict)
        self.assertIn('updated_at', review_dict)

    def test_invalid_rating_on_init(self):
        with self.assertRaises(ValueError):
            Review("Bad rating", 6, "user123", "place456")

if __name__ == '__main__':
    unittest.main()