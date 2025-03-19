import os
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

app = Flask(__name__)
api = Api(app)

# In-memory database for storing users
users = {}

# Configure upload folder for CSV file
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# User model
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# POST API to create a user
class CreateUser(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        
        if not name or not age:
            return {"message": "Both 'name' and 'age' are required"}, 400

        user = User(name, age)
        users[name] = user
        return {"message": "User created successfully"}, 201

# DELETE API to delete a specific user by name
class DeleteUser(Resource):
    def delete(self, name):
        if name in users:
            del users[name]
            return {"message": f"User {name} deleted successfully"}, 200
        return {"message": f"User {name} not found"}, 404

# GET API to list all users
class ListUsers(Resource):
    def get(self):
        user_list = [{"name": user.name, "age": user.age} for user in users.values()]
        return jsonify(user_list)

# POST API to add users from CSV file
class AddUsersFromCSV(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"message": "No file part"}, 400
        file = request.files['file']
        
        if file.filename == '' or not allowed_file(file.filename):
            return {"message": "Invalid file type. Please upload a CSV file."}, 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Read CSV and add users
        try:
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                name = row.get('name')
                age = row.get('age')
                if name and age:
                    user = User(name, age)
                    users[name] = user
            return {"message": "Users added from CSV successfully."}, 200
        except Exception as e:
            return {"message": f"Error processing CSV: {str(e)}"}, 500

# GET API to calculate average age by the first character of the username
class CalculateAverageAge(Resource):
    def get(self):
        # Group users by the first letter of their name
        groups = {}
        for user in users.values():
            first_letter = user.name[0].upper()
            if first_letter not in groups:
                groups[first_letter] = []
            groups[first_letter].append(user.age)
        
        # Calculate average age for each group
        averages = {}
        for group, ages in groups.items():
            average_age = sum(ages) / len(ages)
            averages[group] = average_age
        
        return jsonify(averages)

# Add API endpoints
api.add_resource(CreateUser, '/users')
api.add_resource(DeleteUser, '/users/<string:name>')
api.add_resource(ListUsers, '/users')
api.add_resource(AddUsersFromCSV, '/users/csv')
api.add_resource(CalculateAverageAge, '/users/average-age')

# Swagger UI setup
@app.route('/swagger')
def swagger_ui():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # Start the server
    app.run(debug=True)
