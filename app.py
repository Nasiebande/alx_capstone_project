from flask import Flask, render_template, request, redirect, url_for
import requests
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Mock user data (in a real application, you would use a database)
users = {
    "user1": {"password": "password1"},
    "user2": {"password": "password2"}
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.favorite_recipes = []
        self.shopping_list = []

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

EDAMAM_APP_ID = "f081e0c8"
EDAMAM_APP_KEY = "cb1eb46dea31ba0c46fb7f96b463fb7d"

# Mock recipe data
recipes = [
    {
        "name": "Pasta Carbonara",
        "ingredients": "Pasta, eggs, bacon, Parmesan cheese",
        "cuisine": "Italian",
        "dish_type": "Pasta",
        "ratings": [],
        "reviews": []
    },
    {
        "name": "Chicken Stir-Fry",
        "ingredients": "Chicken, vegetables, soy sauce, ginger",
        "cuisine": "Chinese",
        "dish_type": "Stir-Fry",
        "ratings": [],
        "reviews": []
    },
    # Add more recipe objects here
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recipe/<int:index>")
def recipe_details(index):
    # Ensure the index is within the range of the recipes list
    if 0 < index <= len(recipes):
        recipe = recipes[index - 1]
        return render_template("recipe_detail.html", recipe=recipe)
    else:
        return "Recipe not found", 404
    
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/add_favorite/<int:index>")
@login_required
def add_favorite(index):
    if 0 < index <= len(recipes):
        recipe = recipes[index - 1]
        current_user.favorite_recipes.append(recipe)
        return redirect(url_for("index"))
    else:
        return "Recipe not found", 404

@app.route("/remove_favorite/<int:index>")
@login_required
def remove_favorite(index):
    if 0 < index <= len(current_user.favorite_recipes):
        del current_user.favorite_recipes[index - 1]
        return redirect(url_for("index"))
    else:
        return "Recipe not found", 404

@app.route("/add_to_shopping_list/<int:index>")
@login_required
def add_to_shopping_list(index):
    if 0 < index <= len(recipes):
        recipe = recipes[index - 1]
        current_user.shopping_list.append(recipe)
        return redirect(url_for("index"))
    else:
        return "Recipe not found", 404
    
@app.route("/recipe/<int:index>/rate", methods=["POST"])
@login_required
def rate_recipe(index):
    rating = int(request.form.get("rating"))
    comment = request.form.get("comment")

    if 0 < index <= len(recipes):
        recipe = recipes[index - 1]
        recipe["ratings"].append(rating)
        recipe["reviews"].append({"user": current_user.id, "comment": comment})
        # Calculate the average rating for the recipe
        average_rating = sum(recipe["ratings"]) / len(recipe["ratings"])
        recipe["average_rating"] = round(average_rating, 1)
        return redirect(url_for("recipe_details", index=index))
    else:
        return "Recipe not found", 404

@app.route("/search", methods=["POST"])
def search():
    search_term = request.form.get("search-term").lower()
    search_type = request.form.get("search-type")
    
    # Construct the Edamam API request
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
    else:
        recipes = []  # Handle the error case gracefully

    return render_template("index.html", recipes=recipes)

if __name__ == "__main__":
    app.run(debug=True)