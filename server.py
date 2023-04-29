import json
import os.path

import time
import datetime
import threading

from mcstatus import JavaServer
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Lock


online_players = {}
playtime_ledger = {}
lock = Lock()
app = Flask(__name__)


@app.route('/online_players')
def get_online_players():
    with lock:
        return jsonify(online_players)


@app.route('/top_players/<int:x>')
def get_top_players(x=5):
    with lock:
        sorted_players = sorted(playtime_ledger.items(), key=lambda item: item[1], reverse=True)
        if x >= len(sorted_players):
            return jsonify(sorted_players)
        else:
            return jsonify(sorted_players[:x])


def handler():
    server = JavaServer("158.62.203.83", 25565)
    while True:
        response = server.status()
        if response.players.sample is not None:
            with lock:
                online_players["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                online_players["players"] = []
                for player in response.players.sample:
                    online_players["players"].append({"name": player.name, "id": player.id})
                    if player.name in playtime_ledger:
                        playtime_ledger[player.name] += 60
                    else:
                        playtime_ledger[player.name] = 60
        save_ledger_to_file()
        time.sleep(60)


def read_ledger_from_file():
    global playtime_ledger
    if os.path.exists("ledger.json"):
        with open("ledger.json", "r") as data:
            with lock:
                playtime_ledger = json.load(data)


def save_ledger_to_file():
    with open("ledger.json", "w") as data:
        data.write(json.dumps(playtime_ledger))


def setup():
    CORS(app)
    read_ledger_from_file()
    thread = threading.Thread(target=handler)
    thread.start()


with app.app_context():
    setup()


if __name__ == "__main__":
    setup()
    app.run()
