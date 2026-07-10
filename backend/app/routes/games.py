"""Game Routes"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.app.models import Game, Score, User

games_bp = Blueprint('games', __name__, url_prefix='/api/games')

@games_bp.route('', methods=['GET'])
def get_games():
    """Get all available games."""
    games = Game.query.filter_by(is_active=True).all()
    return jsonify([game.to_dict() for game in games]), 200

@games_bp.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    """Get game details."""
    game = Game.query.get(game_id)
    
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    return jsonify(game.to_dict()), 200

@games_bp.route('/<int:game_id>/submit-score', methods=['POST'])
@jwt_required()
def submit_score(game_id):
    """Submit a game score."""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        score = Score(
            user_id=user_id,
            game_id=game_id,
            score=data.get('score', 0),
            duration=data.get('duration'),
            level=data.get('level', 1),
            difficulty=data.get('difficulty', 'normal'),
            is_multiplayer=data.get('is_multiplayer', False)
        )
        
        user.total_score += score.score
        user.games_played += 1
        
        db.session.add(score)
        db.session.commit()
        
        return jsonify({
            'message': 'Score submitted successfully',
            'score': score.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
