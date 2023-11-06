# Import necessary modules and libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
import os

# Create a Flask application
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Define a user loader function
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id) 
    return user

# Define user information
users = {
    "user1": {"password": "password1"},
    "user2": {"password": "password2"}
}

# Define a User class with user information
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.favorite_recipes = []
        self.shopping_list = []

# Define Edamam API credentials
EDAMAM_APP_ID = "f081e0c8"
EDAMAM_APP_KEY = "cb1eb46dea31ba0c46fb7f96b463fb7d"

# Initialize an empty list for recipes
recipes = [] 

# Fetch recipes from Edamam or your source and populate the global recipes list
def fetch_recipes_from_edamam():
    global recipes
    recipes = fetch_recipes_from_edamam()  # Function to fetch recipes

# Define the main route to display the homepage
@app.route("/")
def index():
    return render_template("index.html")

# Define the login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html")

# Define the logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# Define the search route to fetch recipes from the Edamam API
@app.route("/search", methods=["POST"])
def search():
    global recipes
    search_term = request.form.get("search-term")

    edamam_url = "https://api.edamam.com/search"
    params = {
        "q": search_term,
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY,
    }

    response = requests.get(edamam_url, params=params)

    if response.status_code == 200:
        data = response.json()
        recipes = data.get("hits", [])
        return render_template("search_results.html", recipes=recipes)
    else:
        return "Error occurred while fetching recipes", 500

# Define the route to view the details of a specific recipe
@app.route("/recipe/<int:index>")
def recipe_details(index):
    if 0 < index <= len(recipes):
        recipe = {'hits': [recipes[index]]}
        image_url = recipe.get("recipe", {}).get("image", "")
        return render_template("recipe_detail.html", recipe=recipe, image_url=image_url)
    else:
        return "Recipe not found", 404

# Define route to add favorite recipes
@app.route("/add_to_favorites/<int:index>", methods=["POST"])
@login_required
def add_favorite(index):
    if 0 < index <= len(recipes):
        recipe = recipes[index - 1]
        current_user.favorite_recipes.append(recipe)
        return redirect(url_for("recipe_details", index=index, anchor="favorites"))
    else:
        return "Recipe not found", 404

# Define route to remove from favorite recipes
@app.route("/remove_from_favorite/<int:index>", methods=["POST"])
@login_required
def remove_favorite(index):
    if 0 < index <= len(current_user.favorite_recipes):
        del current_user.favorite_recipes[index - 1]
        return redirect(url_for("index"))
    else:
        return "Recipe not found", 404

# Define route to add to shopping list
@app.route("/add_to_shopping_list/<int:index>", methods=["POST"])
@login_required
def add_to_shopping_list(index):
    if 0 < index <= len(recipes):
        recipe = recipes[index - 1]
        current_user.shopping_list.append(recipe)
        return redirect(url_for("index"))
    else:
        return "Recipe not found", 404
    
# Define route to add review
@app.route("/add_review/<int:recipe_id>", methods=["POST"])
@login_required
def add_review(recipe_id):
    rating = int(request.form["rating"])
    review_text = request.form["review"]
    return redirect(url_for("recipe_details", recipe_id=recipe_id))

# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
