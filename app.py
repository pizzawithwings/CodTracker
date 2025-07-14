import os
from flask import Flask, request, jsonify

app = Flask(__name__)

matches = []
leaderboard = {}

@app.route('/')
def home():
    return "Welcome to COD 1v1 Leaderboard API! Use /leaderboard or /matches endpoints."

@app.route('/submit_match', methods=['POST'])
def submit_match():
    data = request.json
    winner = data.get('winner')
    loser = data.get('loser')
    category = data.get('category')
    if not winner or not loser or not category:
        return jsonify({'error': 'Missing required fields'}), 400
    matches.append(data)
    leaderboard[winner] = leaderboard.get(winner, 0) + 1
    return jsonify({'status': 'success', 'message': 'Match submitted'})

@app.route('/matches', methods=['GET'])
def get_matches():
    return jsonify(matches)

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    return jsonify(leaderboard)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
