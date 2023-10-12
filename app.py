from flask import Flask, render_template, request

app = Flask(__name__)

# Mock recipe data
recipes = [
    {
        "name": "Pasta Carbonara",
        "ingredients": "Pasta, eggs, bacon, Parmesan cheese",
        "cuisine": "Italian",
        "dish_type": "Pasta"
    },
    {
        "name": "Chicken Stir-Fry",
        "ingredients": "Chicken, vegetables, soy sauce, ginger",
        "cuisine": "Chinese",
        "dish_type": "Stir-Fry"
    },
]

@app.route("/")
def index():
    return render_template("index.html", recipes=recipes)

@app.route("/search", methods=["POST"])
def search():
    search_term = request.form.get("search-term").lower()
    search_type = request.form.get("search-type")
    
    filtered_recipes = []
    
    for recipe in recipes:
        if search_type == "name" and search_term in recipe["name"].lower():
            filtered_recipes.append(recipe)
        elif search_type == "ingredients" and search_term in recipe["ingredients"].lower():
            filtered_recipes.append(recipe)
        elif search_type == "cuisine" and search_term in recipe["cuisine"].lower():
            filtered_recipes.append(recipe)
    
    return render_template("index.html", recipes=filtered_recipes)

if __name__ == "__main__":
    app.run(debug=True)