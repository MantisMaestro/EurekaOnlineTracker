import asyncio
import datetime
import logging

import firestore_service
from mcstatus import JavaServer

fsService = firestore_service.FirestoreService()
logger = logging.getLogger('eureka_monitor')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('eureka_monitor.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s -:- %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


async def handler():
    try:
        server = JavaServer("158.62.203.83", 25565)
        while True:
            online_players = {}
            response = server.status()
            logger.info("{} player(s) online".format(response.players.online))
            if response.players.sample is not None:
                online_players["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                online_players["players"] = []
                for player in response.players.sample:
                    online_players["players"].append({"name": player.name, "id": player.id})
                    logger.info("Retrieved status information for {}".format(player.name))
                save_ledger_to_firestore(online_players)
                save_online_players_to_firestore(online_players)
            await asyncio.sleep(1)
    except Exception:
        logger.critical("An error occured in the server_handler.handler()")


def save_online_players_to_firestore(data):
    fsService.update_or_add_online_players(data)


def save_ledger_to_firestore(data):
    fsService.update_or_add_player_time_ledger(data)


def setup():
    logger.info("Logging successfully started...")


def main():
    setup()
    loop = asyncio.get_event_loop()
    while True:
        try:
            asyncio.set_event_loop(loop)
            loop.run_until_complete(handler())
        except:
            logger.error("There was an error running the loop.")


if __name__ == "__main__":
    main()
