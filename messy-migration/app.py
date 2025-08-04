from flask import Flask, request, jsonify, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'users.db'
app = Flask(__name__)

def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return jsonify({"message": "User Management System"}), 200

# Other routes: get_all_users, get_user, create_user, update_user, delete_user, search_users, login
# (Use the exact route implementations you shared earlier, including the email check on update_user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
