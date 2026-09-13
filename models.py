# Defines User and Note database models

from extensions import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False) #Ensure username is unique
    _password_hash = db.Column('password_hash', db.String, nullable=False) # Ensure password is hashed
    note = db.relationship('Note', backref='user', cascade='all, delete-orphan') #Link user to a note

    @property
    def password_hash(self): # prevents direct access to stored password hash
        raise AttributeError('password_hash is not readable')

    @password_hash.setter 
    def password_hash(self, password): # hash passsword before storing it 
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password): #check password against stored hash
        return bcrypt.check_password_hash(self._password_hash, password)

class Note(db.Model): #Link note to user 
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)