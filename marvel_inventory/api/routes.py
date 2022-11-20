from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, Character, character_schema, characters_schema


api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata', methods = ['GET'])
@token_required
def getdata(current_user_token):
    return {'some':'value'}

# Create Character
@api.route('/characters', methods = ['POST'])
@token_required
def create_character(current_user_token):
    id = request.json['id']
    name = request.json['name']
    desc = request.json['desc']
    num_comics = request.json['num_comics']
    num_stories = request.json['num_stories']
    num_series = request.json['num_series']
    user_token = current_user_token.token

    character = Character(id, name, desc, num_comics, num_series, num_stories, user_token=user_token)

    db.session.add(character)
    db.session.commit()
    return jsonify(character_schema.dump(character))

# Get All characters
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token=owner).all()
    return jsonify(characters_schema.dump(characters))

# Get One Character
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        character = Character.query.get(id)
        return jsonify(character_schema.dump(character))
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# Update
@api.route('/characters/<id>', methods = ['POST', 'PUT'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id)
    character.name = request.json['name']
    character.desc = request.json['desc']
    character.num_comics = request.json['num_comics']
    character.num_stories = request.json['num_stories']
    character.num_series = request.json['num_series']
    character.user_token = current_user_token.token

    db.session.commit()
    return jsonify(character_schema.dump(character))

# Delete
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    return jsonify(character_schema.dump(character))
