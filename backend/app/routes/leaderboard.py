"""Leaderboard Routes"""

from flask import Blueprint, request, jsonify
from sqlalchemy import func
from backend.app import db
from backend.app.models import User, Score, Game

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/api/leaderboard')

@leaderboard_bp.route('/global', methods=['GET'])
def global_leaderboard():
    """Get global leaderboard (top users by total score)."""
    limit = request.args.get('limit', 100, type=int)
    
    users = User.query.filter_by(is_active=True).order_by(
        User.total_score.desc()
    ).limit(limit).all()
    
    leaderboard = []
    for rank, user in enumerate(users, 1):
        user_data = user.to_dict()
        user_data['rank'] = rank
        leaderboard.append(user_data)
    
    return jsonify(leaderboard), 200

@leaderboard_bp.route('/game/<int:game_id>', methods=['GET'])
def game_leaderboard(game_id):
    """Get leaderboard for a specific game."""
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    limit = request.args.get('limit', 100, type=int)
    
    # Get top scores per player
    subquery = db.session.query(
        Score.user_id,
        func.max(Score.score).label('max_score')
    ).filter_by(game_id=game_id).group_by(Score.user_id).subquery()
    
    top_scores = db.session.query(
        User.id,
        User.username,
        User.display_name,
        subquery.c.max_score
    ).join(subquery, User.id == subquery.c.user_id).order_by(
        subquery.c.max_score.desc()
    ).limit(limit).all()
    
    leaderboard = []
    for rank, (user_id, username, display_name, score) in enumerate(top_scores, 1):
        leaderboard.append({
            'rank': rank,
            'user_id': user_id,
            'username': username,
            'display_name': display_name,
            'score': score
        })
    
    return jsonify(leaderboard), 200
