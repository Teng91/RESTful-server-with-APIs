import unittest
from app import app, users  # 確保 users 變數在 app.py 是可導入的

class TestCreateUserAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
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
        
    def test_create_user_valid(self):
        response = self.app.post('/create_user', data={'name': 'TestUser', 'age': 25})
        self.assertEqual(response.status_code, 200)
        self.assertIn('User created successfully', response.data.decode())

    def test_delete_user_valid(self):
        # 先創建一個用戶
        self.app.post('/create_user', data={'name': 'TestUser', 'age': 25})
        # 刪除用戶
        response = self.app.delete('/delete_user', data={'name': 'TestUser'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted successfully', response.data.decode())

    def test_delete_user_not_found(self):
        response = self.app.delete('/delete_user', data={'name': 'NonExistentUser'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.data.decode())

    def test_get_users_empty(self):
        response = self.app.get('/get_users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_users_with_data(self):
        # 先創建一個用戶
        self.app.post('/create_user', data={'name': 'TestUser', 'age': 25})
        # 獲取用戶列表
        response = self.app.get('/get_users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'TestUser')
        self.assertEqual(response.json[0]['age'], 25)

if __name__ == '__main__':
    unittest.main()
