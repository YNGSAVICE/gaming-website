"""Achievement Model"""

from datetime import datetime
from backend.app import db

user_achievements = db.Table(
    'user_achievements',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievements.id'), primary_key=True),
    db.Column('earned_at', db.DateTime, default=datetime.utcnow)
)

class Achievement(db.Model):
    """Achievement model for gamification."""
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon_url = db.Column(db.String(255), nullable=True)
    requirement = db.Column(db.String(255), nullable=True)
    points = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert achievement to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon_url': self.icon_url,
            'points': self.points,
        }
    
    def __repr__(self):
        return f'<Achievement {self.name}>'
