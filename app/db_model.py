from app import db

# Define the User model to represent users in the database
class User(db.Model):
    """
    Represents a user in the system.
    - `id`: Unique identifier for each user.
    - `username`: The username of the user (must be unique and not nullable).
    - `password`: The hashed password of the user.
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for the user
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username must be unique and cannot be null
    password = db.Column(db.String(200), nullable=False)  # Password (hashed for security)

# Define the Task model to represent tasks in the database
class Task(db.Model):
    """
    Represents a task in the system.
    - `id`: Unique identifier for each task.
    - `title`: The title of the task (cannot be null).
    - `description`: Optional detailed description of the task.
    - `user_id`: Foreign key linking the task to a specific user.
    - `user`: Relationship to the User model for easy access to the associated user.
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for the task
    title = db.Column(db.String(80), nullable=False)  # Task title, cannot be null
    description = db.Column(db.String(200))  # Optional description of the task
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key referencing the User table

    # Define a relationship with the User model
    # Backref allows easy access to a user's tasks (e.g., `user.tasks`)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
