import asyncio
import datetime
from mcstatus import JavaServer
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Lock, Thread


app = Flask(__name__)
CORS(app)
lock = Lock()

online_players = {}
playtime_ledger = {}


@app.route('/online_players')
def get_online_players():
    with lock:
        return jsonify(online_players)


@app.route('/top_players/<int:x>')
def get_top_players(x):
    with lock:
        sorted_players = sorted(playtime_ledger.items(), key=lambda item: item[1], reverse=True)
        if x >= len(sorted_players):
            return jsonify(sorted_players)
        else:
            return jsonify(sorted_players[:x])


async def handler():
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
        await asyncio.sleep(60)
          
          
def main():
    print("Starting Eureka Online Tracker...")
    
    def run_handler():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(handler())
    
    handler_thread = Thread(target=run_handler)
    handler_thread.start()
    
    app.run()
    print("Eureka Online Tracker Started Successfully...")
          
            
if __name__ == "__main__":
    main()
    