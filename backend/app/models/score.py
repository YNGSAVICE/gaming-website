"""Score Model"""

from datetime import datetime
from backend.app import db

class Score(db.Model):
    """Score model for tracking game scores."""
    __tablename__ = 'scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=True)  # In seconds
    level = db.Column(db.Integer, default=1)
    difficulty = db.Column(db.String(50), nullable=True)  # e.g., 'easy', 'medium', 'hard'
    is_multiplayer = db.Column(db.Boolean, default=False)
    opponent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert score to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'game_id': self.game_id,
            'score': self.score,
            'duration': self.duration,
            'level': self.level,
            'difficulty': self.difficulty,
            'is_multiplayer': self.is_multiplayer,
            'created_at': self.created_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<Score {self.user_id} - {self.score}>'
