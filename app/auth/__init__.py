from flask import Blueprint

# Create a Blueprint for the authentication module and this organizes routes related to user authentication
auth_bp = Blueprint('auth', __name__)

# Import the user login and signup route definitions from their respective files.
from app.auth import user_login, user_signup
