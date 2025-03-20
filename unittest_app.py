import unittest
from app import app

class TestCreateUserAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_user_empty_name(self):
        response = self.app.post('/create_user', data={'name': '', 'age': 25})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Name is required', response.data.decode())

    def test_create_user_age_out_of_range(self):
        response = self.app.post('/create_user', data={'name': 'TestUser', 'age': 999})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Age out of range', response.data.decode())

if __name__ == '__main__':
    unittest.main()