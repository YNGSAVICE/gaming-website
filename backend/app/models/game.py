"""Game Model"""

from datetime import datetime
from backend.app import db

class Game(db.Model):
    """Game model for different game types."""
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    game_type = db.Column(db.String(50), nullable=False)  # e.g., 'puzzle', 'action', 'strategy'
    icon_url = db.Column(db.String(255), nullable=True)
    max_players = db.Column(db.Integer, default=1)
    min_score = db.Column(db.Integer, default=0)
    max_score = db.Column(db.Integer, default=100)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    scores = db.relationship('Score', backref='game', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert game to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_type': self.game_type,
            'icon_url': self.icon_url,
            'max_players': self.max_players,
            'is_active': self.is_active,
        }
    
    def __repr__(self):
        return f'<Game {self.name}>'
