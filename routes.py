# Contains the API routes for authentication and note management

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models import User, Note

bp = Blueprint('routes', __name__)

# Authentication routes 
@bp.route('/signup', methods=['POST']) # Create new user and return access token
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'username already taken'}), 400
    user = User(username=username)
    user.password_hash = password
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.id))
    return jsonify({'user': {'id': user.id,'username': user.username}, 'token': token}), 201

@bp.route('/login', methods=['POST']) # Verify user and return access token
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.authenticate(password):
        return jsonify({'error', 'invalid username or password'}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({'user': {'id': user.id,'username': user.username}, 'token': token}), 200

@bp.route('/me', methods=['GET']) # Return details of authenticated user
@jwt_required() 
def me():
    user = User.query.get(int(get_jwt_identity()))
    return jsonify({'id': user.id, 'username': user.username}), 200

# Note routes 
@bp.route('/notes', methods=['GET']) # Return authenticated user notes with pagination
@jwt_required()
def get_notes():
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = Note.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        'notes': [{'id': n.id,'title': n.title, 'content': n.content} for n in pagination.items],
        'page': pagination.page,
        'total_pages': pagination.pages,
        'total_notes': pagination.total
    }), 200


@bp.route('/notes', methods=['POST']) # Create new note for authenticated user
@jwt_required()
def create_note():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'error': 'title and content are required'}), 400
    note = Note(title=title, content=content, user_id=user_id)
    db.session.add(note)
    db.session.commit()
    return jsonify({'id': note.id, 'title': note.title, 'content': note.content}), 201


@bp.route('/notes/<int:note_id>', methods=['PATCH']) # Update note for authenticated user
@jwt_required()
def update_note(note_id):
    user_id = int(get_jwt_identity())
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': 'note not found'}), 404
    data = request.get_json()
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    db.session.commit()
    return jsonify({'id': note.id, 'title': note.title, 'content': note.content}), 200

@bp.route('/notes/<int:note_id>', methods=['DELETE']) # Delete note for authenticated user
@jwt_required()
def delete_note(note_id):
    user_id = int(get_jwt_identity())
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': 'note not found'}), 404
    db.session.delete(note)
    db.session.commit()
    return {}, 204
