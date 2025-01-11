# Run this file to start the application
from app import create_app, db

app = create_app()

# Ensure database tables are created
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
