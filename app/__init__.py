from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask
from datetime import datetime

from app.extensions import db, login_manager




def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Jinja global
    app.jinja_env.globals['current_year'] = datetime.now().year

    # Register blueprints (AFTER extensions)
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.google import google_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(google_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
