from flask import request, jsonify
from app import db
from app.db_model import User
from flask_bcrypt import Bcrypt
from app.auth import auth_bp

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Define the signup route under the auth Blueprint
@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Handles user registration by validating input, hashing the password, and saving the user to the database.

    """

    # Parse the JSON data sent in the request body
    data = request.get_json()
    username = data.get('username')  # Extract the username
    password = data.get('password')  # Extract the password

    # Validate password complexity
    # Requirements:
    # - At least 8 characters
    # - At least one uppercase letter
    # - At least one lowercase letter
    # - At least one number
    # - At least one special character
    if len(password) < 8 or \
       not any(c.isupper() for c in password) or \
       not any(c.islower() for c in password) or \
       not any(c.isdigit() for c in password) or \
       not any(c in "!@#$%^&*()_+" for c in password):
        return jsonify({
            "error": "Password must be at least 8 characters long and include an uppercase letter, "
                     "a lowercase letter, a number, and a special character."
        }), 400

    # Hash the password for secure storage in the database
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if the username already exists in the database
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    # Create a new user object and save it to the database
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)  # Add the new user to the database session
    db.session.commit()  # Commit the transaction to save the user

    # Return a success message
    return jsonify({"message": "User registered successfully!"}), 201
