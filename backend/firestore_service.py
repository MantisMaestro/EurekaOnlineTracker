import datetime
import logging

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirestoreService:
    def __init__(self):
        self.cred = credentials.Certificate('eurekaonline-bdcf2-firebase-adminsdk-sbr8z-1d1449d966.json')
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        logger = logging.getLogger('firestore_service')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler('firestore_service.log')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s -:- %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    def update_or_add_online_players(self, online_players):
        docs = self.db.collection('online_now').stream()
        for doc in docs:
            doc.delete()
        for player in online_players['players']:
            logger.info(f"Player online: {player['name']}")
            self.db.collection('online_now').document(player['uid']).set(player)

    def update_or_add_player_time_ledger(self, online_players):
        docs = self.db.collection('players').stream()
        for player in online_players['players']:
            if all(doc.id != player['uid'] for doc in docs):
                new_player = {
                    "last_online": datetime.datetime.now(),
                    "name": player["name"],
                    "time_online_seconds": 0
                }
                logger.info(f"New player added to ledger: {player['name']}")
                self.db.collection('players').document(player['uid']).set(new_player)
            else:
                logger.info(f"Player ledger updated: {player['name']}")
                self.db.collection('players').document(player['uid']).update(
                    {'time_online_seconds': firestore.Increment(60),
                     'last_online': datetime.datetime.now()}
                )

    def get_player_ledger(self):
        docs = self.db.collection('players').stream()
        data = []
        for doc in docs:
            data.append(doc.to_dict())
        ledger = {"players": data}
        return ledger

    def get_online_players(self):
        docs = self.db.collection('online_now').stream()
        data = []
        for doc in docs:
            data.append(doc.to_dict())
        online = {"players": data}
        return online
