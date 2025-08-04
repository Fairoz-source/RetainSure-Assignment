from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__)

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    if not email or not password:
        return jsonify({'error': 'Missing fields'}), 400
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid credentials'}), 401
