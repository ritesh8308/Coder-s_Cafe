from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Set configuration (secret key + database path)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafemanager.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register models and create tables
    with app.app_context():
        from .models import models  # Loads models from models.py
        db.create_all()


    from .routes.menu import menu_bp
    app.register_blueprint(menu_bp)

    from .routes.order import order_bp
    app.register_blueprint(order_bp)


    # TODO: Register blueprints here later (menu, order, billing)
    return app
