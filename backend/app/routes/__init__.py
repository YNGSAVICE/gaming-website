"""Flask Routes/Blueprints"""

from .auth import auth_bp
from .users import users_bp
from .games import games_bp
from .leaderboard import leaderboard_bp

__all__ = ['auth_bp', 'users_bp', 'games_bp', 'leaderboard_bp']
