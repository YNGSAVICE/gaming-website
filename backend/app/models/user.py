"""User Model"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.app import db

class User(db.Model):
    """User model for authentication and profile management."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(120), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    total_score = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    scores = db.relationship('Score', backref='player', lazy=True, cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', secondary='user_achievements', backref='users')
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'display_name': self.display_name,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'total_score': self.total_score,
            'games_played': self.games_played,
            'created_at': self.created_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
