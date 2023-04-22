import json
import os.path

import asyncio
import datetime
from mcstatus import JavaServer
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Lock, Thread


app = Flask(__name__)


class EurekaOnlineTracker:
    def __init__(self):
        self.online_players = {}
        self.playtime_ledger = {}
        self.lock = Lock()

    def get_online_players(self):
        with self.lock:
            return jsonify(self.online_players)

    def get_top_players(self, x):
        with self.lock:
            sorted_players = sorted(self.playtime_ledger.items(), key=lambda item: item[1], reverse=True)
            if x >= len(sorted_players):
                return jsonify(sorted_players)
            else:
                return jsonify(sorted_players[:x])

    async def handler(self):
        server = JavaServer("158.62.203.83", 25565)
        while True:
            response = server.status()
            if response.players.sample is not None:
                with self.lock:
                    self.online_players["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.online_players["players"] = []
                    for player in response.players.sample:
                        self.online_players["players"].append({"name": player.name, "id": player.id})
                        if player.name in self.playtime_ledger:
                            self.playtime_ledger[player.name] += 60
                        else:
                            self.playtime_ledger[player.name] = 60
            self.save_ledger_to_file()
            await asyncio.sleep(60)

    def read_ledger_from_file(self):
        if os.path.exists("ledger.json"):
            with open("ledger.json", "r") as data:
                with self.lock:
                    self.playtime_ledger = json.load(data)

    def save_ledger_to_file(self):
        with open("ledger.json", "w") as data:
            data.write(json.dumps(self.playtime_ledger))


def main():
    tracker = EurekaOnlineTracker()
    tracker.read_ledger_from_file()

    def run_handler():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(tracker.handler())

    handler_thread = Thread(target=run_handler)
    handler_thread.start()
    
    CORS(app)

    app.add_url_rule('/online_players', 'get_online_players', tracker.get_online_players)
    app.add_url_rule('/top_players/<int:x>', 'get_top_players', tracker.get_top_players)

    app.run()


if __name__ == "__main__":
    main()
