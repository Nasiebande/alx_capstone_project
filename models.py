# Import necessary modules
from database import db
from flask_login import UserMixin

# Define a table for user's favorite recipes
user_favorite_recipes = db.Table(
    'user_favorite_recipes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

# Define a table for user's shopping list
user_shopping_list = db.Table(
    'user_shopping_list',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

# Define the User class with necessary attributes and relationships
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    favorite_recipes = db.relationship('Recipe', secondary=user_favorite_recipes)
    shopping_list = db.relationship('Recipe', secondary=user_shopping_list)

# Define the Recipe class with necessary attributes
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    cuisine = db.Column(db.String(100))
    dish_type = db.Column(db.String(100))
    cooking_time = db.Column(db.Integer)

    # Define relationships for ratings and reviews
    ratings = db.relationship('Rating', backref='recipe')
    reviews = db.relationship('Review', backref='recipe')

# Define the Rating class with necessary attributes
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)

    # Define foreign key relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

# Define the Review class with necessary attributes
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)

    # Define foreign key relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))