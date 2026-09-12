# This is the entry point for the backend system.

from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, migrate, jwt

import models # Allows database migrations

# Create the Flask app
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # Database location
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable change tracking
    app.config['JWT_SECRET_KEY'] = 'dev-secret-change-me' # JWT secret keys

    db.init_app(app) # Connects SQLAlchemy to the app
    bcrypt.init_app(app) # Enables password hashing
    migrate.init_app(app, db) # For database migrations
    jwt.init_app(app) # enable JWT authentication
    CORS(app) # Allows app to get requests from the front end

    from routes import bp
    app.register_blueprint(bp) #Registers app routes 
    return app

app = create_app

# Start development server 
if __name__ == '__main__':
    app.run(port=5555, debug=True)