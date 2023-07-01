from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Lock
import firestore_service
from datetime import datetime


online_players = {}
playtime_ledger = {}
lock = Lock()
app = Flask(__name__)
fsService = firestore_service.FirestoreService("fsService-api")


@app.route('/online_players')
def get_online_players():
    response = fsService.get_online_players()
    return jsonify(response)


@app.route('/top_players/<int:x>')
def get_top_players(x=5):
    from_date_str = request.args.get('from_date')
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d') if from_date_str else None
    to_date_str = request.args.get('to_date')
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d') if to_date_str else None
    response = fsService.get_consolidated_ledger(from_date, to_date)
    return jsonify(response)


# @app.route('/top_players/<string:period>/<int:x>')
# def get_top_players_period(period="week", x=5):
#     print("Hello World")
#     response = fsService.get_player_ledger()
#     return jsonify(response)


def setup():
    CORS(app)


with app.app_context():
    setup()


if __name__ == "__main__":
    setup()
    app.run()
