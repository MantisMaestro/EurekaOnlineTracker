import datetime
import threading
import time
import firestore_service

from threading import Lock
from mcstatus import JavaServer

lock = Lock()
online_players = {}
playtime_ledger = {}


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
        time.sleep(60)


def save_ledger_to_firestore():
    print("mlem")
    # FirestoreService.update_or_add_player_time_ledger(online_players=online_players)


def setup():
    thread = threading.Thread(target=handler)
    thread.start()


if __name__ == "__main__":
    setup()
