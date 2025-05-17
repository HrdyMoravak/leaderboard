from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__)
CORS(app)

# Omezování požadavků (rate limit)
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per minute"])


# Nastavení API klíče
API_KEY = "tajnyklic123"

# Cesta k souboru se skóre
SCORES_FILE = "scores.json"

# Funkce pro načtení dat
def load_scores():
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

# Funkce pro uložení dat
def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

# Hlavní stránka
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# Statické soubory (CSS, JS atd.)
@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

# Získání všech skóre (GET)
@app.route("/api/scores", methods=["GET"])
@limiter.limit("100/minute")
def get_scores():
    scores = load_scores()
    return jsonify(scores)

# Zaslání skóre (POST)
@app.route("/api/score", methods=["POST"])
@limiter.limit("5/minute")
def submit_score():
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 403

    data = request.get_json()
    name = data.get("name")
    score = data.get("score")

    if not name or not isinstance(score, int):
        return jsonify({"error": "Invalid data"}), 400

    scores = load_scores()
    current_score = scores.get(name, 0)

    if score > current_score:
        scores[name] = score
        save_scores(scores)

    return jsonify({"message": "Score updated", "scores": scores}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

