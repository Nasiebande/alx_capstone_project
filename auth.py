from database import db
from models import User

def register_user(username, password):
    # Check if the username already exists
    user = User.query.filter_by(id=username).first()
    if user is not None:
        return "Username already exists"
    
    # Create a new User instance and save it to the database
    new_user = User(id=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return "Registration successful"

def verify_password(username, password):
    user = User.query.filter_by(id=username).first()
    if user and user.password == password:
        return True
    return False