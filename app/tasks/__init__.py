from flask import Blueprint

tasks_bp = Blueprint('tasks', __name__)

# Import the task management module to register routes and functionality for task operations
from app.tasks import task_manage
