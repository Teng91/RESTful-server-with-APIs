from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger
import pandas as pd
import os
import unittest

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# 用戶數據存儲
users = []

class CreateUser(Resource):
    def post(self):
        """
        創建用戶
        ---
        parameters:
          - name: name
            in: formData
            type: string
            required: false
            description: 用戶名稱
          - name: age
            in: formData
            type: integer
            required: true
            description: 用戶年齡
        responses:
          200:
            description: 用戶創建成功
        """
        data = request.form
        name = data.get('name')
        age = data.get('age')
        
        if not age:
            return {"message": "Age is required"}, 400 # 一定要輸入年齡
        
        try:
            age = int(age)
        except ValueError:
            return jsonify({'error': 'Age must be an integer'}), 400
        
        if age < 0 or age > 125:
            return {"message": "Age out of range"}, 400 # 設定年齡的合理區間
        
        if not name:
            return {"message": "Name is required but user created"}, 200 # 允許在不輸入名字的情況下創建用戶，但會返回提示用戶名稱是必需
        
        users.append({"name": name, "age": age})
        return {"message": "User created successfully"}, 200

class DeleteUser(Resource):
    def delete(self):
        """
        刪除用戶
        ---
        parameters:
          - name: name
            in: formData
            type: string
            required: true
            description: 用戶名稱
        responses:
          200:
            description: 用戶刪除成功
        """
        data = request.form
        name = data.get('name')
        global users
        users = [user for user in users if user['name'] != name]
        return {"message": "User deleted successfully"}, 200

class GetUsers(Resource):
    def get(self):
        """
        獲取用戶列表
        ---
        responses:
          200:
            description: 返回用戶列表
        """
        return jsonify(users)

class BulkAddUsers(Resource):
    def post(self):
        """
        批量添加用戶
        ---
        parameters:
          - name: file
            in: formData
            type: file
            required: true
            description: 包含用戶數據的 CSV 文件
        responses:
          200:
            description: 用戶批量添加成功
        """
        file = request.files.get('file')
        if not file:
            return {"message": "CSV file is required"}, 400
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            users.append({"name": row['Name'], "age": int(row['Age'])}) # 匯入csv要注意欄位名稱大小寫，匯入後的鍵值對都是小寫
        return {"message": "Users added successfully"}, 200

class AverageAge(Resource):
    def get(self):
        """
        計算每組用戶的平均年齡
        ---
        responses:
          200:
            description: 返回每組用戶的平均年齡
        """
        if not users:
            return {"message": "No users available"}, 400
        df = pd.DataFrame(users)
        df['group'] = df['name'].str[0].str.upper()
        result = df.groupby('group')['age'].mean().to_dict()
        return jsonify(result)

class TestCreateUserAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        global users
        users = []  # 每次測試前清空user列表

    def test_create_user_empty_name(self):
        response = self.app.post('/create_user', data={'name': '', 'age': 25})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Name is required but user created', response.data.decode())

    def test_create_user_age_out_of_range(self):
        response = self.app.post('/create_user', data={'name': 'TestUser', 'age': 999})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Age out of range', response.data.decode())


# 註冊 API 路由
api.add_resource(CreateUser, '/create_user')
api.add_resource(DeleteUser, '/delete_user')
api.add_resource(GetUsers, '/get_users')
api.add_resource(BulkAddUsers, '/bulk_add_users')
api.add_resource(AverageAge, '/average_age')

if __name__ == '__main__':
    app.run()