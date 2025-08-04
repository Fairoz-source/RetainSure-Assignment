from flask import Blueprint, request, jsonify, redirect, abort
from .services import shorten_url, get_original_url, get_stats

bp = Blueprint('routes', __name__)

@bp.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400
    try:
        result = shorten_url(url)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    url = get_original_url(short_code)
    if not url:
        abort(404)
    return redirect(url)

@bp.route("/api/stats/<short_code>", methods=["GET"])
def stats(short_code):
    result = get_stats(short_code)
    if not result:
        abort(404)
    return jsonify(result), 200
