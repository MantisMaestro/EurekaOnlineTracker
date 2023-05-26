from datetime import date, timedelta
import logging

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirestoreService:
    def __init__(self, log_filename="fsService"):
        self.cred = credentials.Certificate('eurekaonline-bdcf2-firebase-adminsdk-sbr8z-1d1449d966.json')
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.logger = logging.getLogger(log_filename)
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(f'{log_filename}.log')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s -:- %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.error("Logging successfully started...")

    def update_or_add_online_players(self, online_players):
        docs = self.db.collection('online_now').stream()
        for doc in docs:
            if all(player['uid'] != doc.id for player in online_players['players']):
                self.logger.error(f"Player no longer online: {doc.id}")
                self.db.collection('online_now').document(doc.id).delete()
        for player in online_players['players']:
            if all(doc.id != player['uid'] for doc in docs):
                self.logger.error(f"Player now online: {player['name']}")
                self.db.collection('online_now').document(player['uid']).set(player)

    def update_or_add_player_time_ledger(self, online_players):
        working_ledger = self.get_working_ledger_id()
        collection = self.db.collection(working_ledger)
        for player in online_players['players']:
            doc_ref = collection.document(player['uid'])
            doc = doc_ref.get()
            if doc.exists:
                self.logger.error(f"Player ledger updated: {player['name']}")
                self.db.collection('players').document(player['uid']).update(
                    {'time_online_seconds': firestore.Increment(60),
                     'last_online': datetime.datetime.now()}
                )
            else:
                new_player = {
                    "last_online": datetime.datetime.now(),
                    "name": player["name"],
                    "time_online_seconds": 0
                }
                self.logger.error(f"New player added to ledger: {player['name']}")
                self.db.collection('players').document(player['uid']).set(new_player)

    def get_player_ledger(self):
        self.logger.error(f"Getting player ledger.")
        working_ledger = self.get_working_ledger_id()
        docs = self.db.collection('players').stream()
        data = []
        for doc in docs:
            data.append(doc.to_dict())
        ledger = {"players": data}
        return ledger

    # def get_consolidated_ledger(self):
    #     ledgers = self.get_week_dates()
    #     consolidated_ledger = {}
    #     for ledger in ledgers:
    #         try:
    #             collection = self.db.collection(ledger).stream()
    #             for doc in collection:
    #                 if doc.id in consolidated_ledger:
    #                     consolidated_ledger[doc.id]["time_online_seconds"] += doc.get('time_online_seconds')#
    #                 else:
    #                     consolidated_ledger[doc.id] = doc.get()
    #         except:
    #             print("Error getting consolidated ledger, does it exist?")

    def get_online_players(self):
        self.logger.error(f"Getting online players.")
        working_ledger = self.get_working_ledger_id()
        docs = self.db.collection('online_now').stream()
        data = []
        for doc in docs:
            data.append(doc.to_dict())
        online = {"players": data}
        return online

    def get_working_ledger_id(self):
        return datetime.today().strftime('%Y-%m-%d')

    # def get_week_dates():
    #     today = date.today()
    #     current_weekday = today.weekday()
    #     monday = today - timedelta(days=current_weekday)
    #     dates = []
    #     for i in range(current_weekday + 1):
    #         day = monday + timedelta(days=i)
    #         dates.append(day.strftime('%Y-%m-%d'))
    #     return dates
