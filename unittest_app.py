import unittest
from app import app, users  # 確保 users 變數在 app.py 是可導入的

class TestCreateUserAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client() # 創建一個測試用的客戶端
        self.app.testing = True
        users.clear()  # 單元測試前清空用戶列表

    def test_create_user_empty_name(self):
        response = self.app.post('/create_user', data={'name': '', 'age': 25})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Name is required but user created', response.data.decode())

    def test_create_user_age_out_of_range(self):
        response = self.app.post('/create_user', data={'name': 'TestUser', 'age': 999})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Age out of range', response.data.decode())

if __name__ == '__main__':
    unittest.main()
