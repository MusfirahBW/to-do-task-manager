from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from app.db_model import User
from app.auth import auth_bp

# Initialize Bcrypt for password hashing and verification
bcrypt = Bcrypt()

# Define the login route under the auth Blueprint
@auth_bp.route('/login', methods=['POST'])
def login():
    
    #Handles user login by verifying credentials and returning a JWT token when testing endpoints using the POST method
    
    # Parse the JSON data sent in the request body
    data = request.get_json()
    username = data.get('username')  # Extract the username
    password = data.get('password')  # Extract the password

    # Query the database to find the user with the given username
    user = User.query.filter_by(username=username).first()

    # If the user does not exist or the password is invalid, return an error response
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password."}), 401

    # Generate a JWT access token using the user's ID as the identity
    token = create_access_token(identity=user.id)

    # Return the generated token in the response
    return jsonify({"token": token}), 200
