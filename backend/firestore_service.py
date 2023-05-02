import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirestoreService:
    def __init__(self):
        self.cred = credentials.Certificate('eurekaonline-bdcf2-firebase-adminsdk-sbr8z-1d1449d966.json')
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def update_or_add_online_players(self, online_players):
        docs = self.db.collection('online_now').stream()
        for doc in docs:
            if all(player['uid'] != doc.id for player in online_players['players']):
                self.db.collection('online_now').document(doc.id).delete()
        for player in online_players['players']:
            if all(doc.id != player['uid'] for doc in docs):
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
                self.db.collection('players').document(player['uid']).set(new_player)
            else:
                self.db.collection('players').document(player['uid']).update(
                    {'time_online_seconds': firestore.Increment(60)}
                )
                
    def get_player_ledger(self):
        docs = self.db.collection('players').stream()
        data = {}
        for doc in docs:
            data[doc.id] = doc.to_dict()
        
    def get_online_players(self):
        docs = self.db.collection('online_now').stream()
        data = {}
        for doc in docs:
            data[doc.id] = doc.to_dict()
        return data
