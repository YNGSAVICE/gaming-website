"""Flask Application Factory"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()

def create_app(config_name='development'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        from backend.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        from backend.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from backend.config import TestingConfig
        app.config.from_object(TestingConfig)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    CORS(app)
    
    # Register blueprints
    from backend.app.routes import auth_bp, users_bp, games_bp, leaderboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(leaderboard_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
