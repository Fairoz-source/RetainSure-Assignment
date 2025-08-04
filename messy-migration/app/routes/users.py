from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

bp = Blueprint('users', __name__)

@bp.route('/users', methods=['GET'])
def get_all_users():
    db = get_db()
    users = db.execute('SELECT id, name, email FROM users').fetchall()
    return jsonify([dict(u) for u in users])

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    db = get_db()
    user = db.execute('SELECT id, name, email FROM users WHERE id = ?', (id,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(user))

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name, email, password = data.get('name'), data.get('email'), data.get('password')
    if not name or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400
    hashed = generate_password_hash(password)
    db = get_db()
    try:
        db.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed))
        db.commit()
        return jsonify({'message': 'User created'}), 201
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            return jsonify({'error': 'Email already exists'}), 409
        return jsonify({'error': str(e)}), 500

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    name, email = data.get('name'), data.get('email')
    if not name or not email:
        return jsonify({'error': 'Missing fields'}), 400
    db = get_db()
    try:
        db.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, id))
        db.commit()
        return jsonify({'message': 'User updated'})
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            return jsonify({'error': 'Email already exists'}), 409
        return jsonify({'error': str(e)}), 500

@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'User deleted'})
