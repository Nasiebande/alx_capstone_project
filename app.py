from flask import Flask, render_template, request

app = Flask(__name__)

# Mock recipe data
recipes = [
    {"name": "Pasta Carbonara", "ingredients": "Pasta, eggs, bacon, Parmesan cheese"},
    {"name": "Chicken Stir-Fry", "ingredients": "Chicken, vegetables, soy sauce, ginger"},
    # Add more recipe objects here
]

@app.route("/")
def index():
    return render_template("index.html", recipes=recipes)

@app.route("/search", methods=["POST"])
def search():
    search_term = request.form.get("search-term").lower()
    filtered_recipes = [recipe for recipe in recipes if search_term in recipe["name"].lower() or search_term in recipe["ingredients"].lower()]
    return render_template("index.html", recipes=filtered_recipes)

if __name__ == "__main__":
    app.run(debug=True)