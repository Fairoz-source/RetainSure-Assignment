from flask import Flask
from app.db import init_app
from app.routes.users import bp as users_bp
from app.routes.auth import bp as auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE="users.db",
        SECRET_KEY="your-secret-key"
    )
    init_app(app)
    app.register_blueprint(users_bp, url_prefix='/api')  # URLs start with /api/users
    app.register_blueprint(auth_bp, url_prefix='/api')   # URLs start with /api/auth

    @app.route("/")
    def health_check():
        return {"message": "User Management System"}, 200

    return app
