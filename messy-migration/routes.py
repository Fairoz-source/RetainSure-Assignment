from flask import Blueprint, request, jsonify, redirect
from .utils import generate_short_code, is_valid_url
from .models import get_db

bp = Blueprint('routes', __name__)

@bp.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    long_url = data.get("url")
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    db = get_db()
    short_code = generate_short_code()
    db.execute("INSERT INTO urls (short_code, long_url) VALUES (?, ?)", (short_code, long_url))
    db.commit()
    return jsonify({"short_url": f"/{short_code}"}), 201

@bp.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    db = get_db()
    result = db.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,)).fetchone()
    if not result:
        return jsonify({"error": "Not found"}), 404
    db.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,))
    db.commit()
    return redirect(result['long_url'])

@bp.route("/api/stats/<short_code>", methods=["GET"])
def stats(short_code):
    db = get_db()
    result = db.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,)).fetchone()
    if not result:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(result))
