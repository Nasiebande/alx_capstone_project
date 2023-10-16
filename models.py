from app import db

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)

    def __init__(self, id, password):
        self.id = id
        self.password = password