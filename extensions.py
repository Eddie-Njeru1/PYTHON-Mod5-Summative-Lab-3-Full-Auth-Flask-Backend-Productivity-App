# Contains the extensions to be shared across the flask the app. 

from flask_sqlalchemy import SQLAlchemy # For database operations
from flask_bcrypt import Bcrypt # For password hashing
from flask_migrate import Migrate # For database migrations
from flask_jwt_extended import JWTManager # For JWT authentication

db = SQLAlchemy() # shared database instance
bcrypt = Bcrypt() # password instance 
migrate = Migrate() # migration instance
jwt = JWTManager() # authentication instance