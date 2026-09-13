# This is the entry point for the entire backend system.

from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, migrate, jwt
import os
import models # Allows database migrations

# Create the Flask app
def create_app():
    app = Flask(__name__)
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    if database_url.startswitch('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url # Database location
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable change tracking
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-change-me') # JWT secret keys

    db.init_app(app) # Connects SQLAlchemy to the app
    bcrypt.init_app(app) # Enables password hashing
    migrate.init_app(app, db) # For database migrations
    jwt.init_app(app) # enable JWT authentication
    CORS(app) # Allows app to get requests from the front end

    from routes import bp
    app.register_blueprint(bp) #Registers app routes 
    return app

app = create_app()

# Start development server 
if __name__ == '__main__':
    app.run(port=5555, debug=True)