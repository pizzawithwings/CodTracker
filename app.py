from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)

# Allow CORS only from your Neocities domain
CORS(app, origins=["https://codtrackerlive.neocities.org"])

# In-memory example data storage
matches = []
leaderboard = {}

# Admin passcode (change as needed)
ADMIN_PASSCODE = "6969"

@app.route('/')
def index():
    return "Welcome to COD 1v1 Leaderboard API!"

@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json()
    passcode = data.get('passcode', '')
    if passcode == ADMIN_PASSCODE:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

@app.route('/matches', methods=['GET', 'POST', 'DELETE'])
def matches_handler():
    if request.method == 'GET':
        # Return all matches
        return jsonify(matches)
    elif request.method == 'POST':
        # Add a new match
        data = request.get_json()
        required = ['winner', 'loser', 'category', 'date']
        if not all(field in data for field in required):
            return jsonify({"error": "Missing fields"}), 400
        matches.append(data)
        return jsonify({"status": "added"}), 201
    elif request.method == 'DELETE':
        # Clear all matches (admin only - for demo, no auth here)
        matches.clear()
        return jsonify({"status": "cleared"})

@app.route('/leaderboard', methods=['GET'])
def leaderboard_handler():
    lb = {}
    for m in matches:
        cat = m.get('category', 'Unknown')
        winner = m.get('winner')
        if cat not in lb:
            lb[cat] = {}
        lb[cat][winner] = lb[cat].get(winner, 0) + 1
    return jsonify(lb)

@app.route('/reset_leaderboard', methods=['DELETE'])
def reset_leaderboard():
    matches.clear()
    return jsonify({"status": "leaderboard reset"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
