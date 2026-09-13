# Populates the database with sample users and notes for testing

from faker import Faker
from app import app
from extensions import db
from models import User, Note

fake = Faker()

with app.app_context():
    Note.query.delete() # remove note
    User.query.delete() # remove user
    users = []
    for _ in range(3):
        user = User(username=fake.unique.user_name())
        user.password_hash = 'password123' #hash the test password
        users.append(user)
        db.session.add(user)
    db.session.commit()

    for user in users:
        for _ in range (4):
            note=Note(
                title=fake.sentence(nb_words=4),
                content=fake.paragraph(nb_sentence=3),
                user_id=user.id
            )
            db.session.add(note)
    db.session.commit() # save all notes 

    print(f'Seeded {len(users)} users with notes:')
    for user in users:
        print(f' {user.username} (id={user.id} - password: password123')
