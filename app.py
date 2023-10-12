from flask import Flask, render_template, request
import requests

app = Flask(__name)

EDAMAM_APP_ID = "f081e0c8"
EDAMAM_APP_KEY = "cb1eb46dea31ba0c46fb7f96b463fb7d"

@app.route("/")
def index():
    return render_template("index.html")

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
        recipes = []

    return render_template("index.html", recipes=recipes)

if __name__ == "__main__":
    app.run(debug=True)