from flask import render_template, jsonify, request
from app import app
from app.game_logic import GameLogic

game_logic = GameLogic()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    game_id, initial_scene = game_logic.start_new_game()
    return jsonify({'game_id': game_id, 'scene': initial_scene})

@app.route('/make_choice', methods=['POST'])
def make_choice():
    data = request.json
    next_scene = game_logic.make_choice(data['game_id'], data['choice'])
    return jsonify({'scene': next_scene})