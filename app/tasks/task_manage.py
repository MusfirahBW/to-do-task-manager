from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.db_model import Task
from app.tasks import tasks_bp

# Route to create a new task
@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required()  # Requires user to be authenticated
def create_task():
    """
    Creates a new task for the authenticated user.
    - Extracts task details from the request body.
    - Associates the task with the currently authenticated user.
    """
    data = request.get_json()
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token

    # Create a new Task instance
    new_task = Task(
        title=data.get('title'),
        description=data.get('description'),
        user_id=current_user_id  # Assign the task to the current user
    )
    db.session.add(new_task)  # Add the task to the database
    db.session.commit()  # Commit the transaction

    return jsonify({"message": "Task created successfully!"}), 201

# Route to retrieve all tasks for the authenticated user
@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()  # Requires user to be authenticated
def get_tasks():
    """
    Retrieves all tasks for the authenticated user.
    - Filters tasks by the user's ID.
    - Returns a list of tasks in JSON format.
    """
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    tasks = Task.query.filter_by(user_id=current_user_id).all()  # Get tasks for the current user
    # Prepare a list of tasks as dictionaries
    tasks_list = [{"id": task.id, "title": task.title, "description": task.description} for task in tasks]
    return jsonify(tasks_list), 200

# Route to retrieve a specific task by ID
@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()  # Requires user to be authenticated
def get_task(task_id):
    """
    Retrieves a specific task by its ID for the authenticated user.
    - Ensures the task belongs to the authenticated user.
    - Returns the task details if found.
    """
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    # Query for the task with the given ID and the current user's ID
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    # Check if the task exists and belongs to the user
    if not task:
        return jsonify({"error": "Task not found or access denied"}), 404

    # Return the task details
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description
    }), 200

# Route to update a specific task
@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()  # Requires user to be authenticated
def update_task(task_id):
    """
    Updates a specific task for the authenticated user.
    - Ensures the task belongs to the authenticated user.
    - Updates the task's title and/or description.
    """
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    # Query for the task with the given ID and the current user's ID
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    # Check if the task exists and belongs to the user
    if not task:
        return jsonify({"error": "Task not found or access denied"}), 404

    # Update task details
    data = request.get_json()
    task.title = data.get('title', task.title)  # Update title if provided
    task.description = data.get('description', task.description)  # Update description if provided
    db.session.commit()  # Commit the transaction

    return jsonify({"message": "Task updated successfully!"}), 200

# Route to delete a specific task
@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()  # Requires user to be authenticated
def delete_task(task_id):
    """
    Deletes a specific task for the authenticated user.
    - Ensures the task belongs to the authenticated user.
    - Deletes the task from the database.
    """
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    # Query for the task with the given ID and the current user's ID
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    # Check if the task exists and belongs to the user
    if not task:
        return jsonify({"error": "Task not found or access denied"}), 404

    # Delete the task from the database
    db.session.delete(task)
    db.session.commit()  # Commit the transaction

    return jsonify({"message": "Task deleted successfully!"}), 200
