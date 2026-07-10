"""User Routes"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.app.models import User, Score

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile."""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_data = user.to_dict()
    user_data['achievements'] = len(user.achievements)
    
    return jsonify(user_data), 200

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user profile."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    user.display_name = data.get('display_name', user.display_name)
    user.bio = data.get('bio', user.bio)
    user.avatar_url = data.get('avatar_url', user.avatar_url)
    
    db.session.commit()
    
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200

@users_bp.route('/<int:user_id>/scores', methods=['GET'])
def get_user_scores(user_id):
    """Get user's game scores."""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.created_at.desc()).paginate(
        page=page, per_page=per_page
    )
    
    return jsonify({
        'scores': [score.to_dict() for score in scores.items],
        'total': scores.total,
        'pages': scores.pages,
        'current_page': page
    }), 200
