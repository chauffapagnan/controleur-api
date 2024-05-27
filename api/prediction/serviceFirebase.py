import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import calendar
import time
from datetime import datetime


def initFirebase():
    cred = credentials.Certificate('credit.json')
    firebase_admin.initialize_app(cred)


def envoieFireBaseWeeklyPrediction(value: str):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(time_stamp)

    db = firestore.client()

    # On Récupère toutes les entrées existantes
    weekly_prediction_ref = db.collection('weekly_prediction')
    docs = weekly_prediction_ref.stream()

    # On Met à jour chaque entrée pour définir enabled à false
    for doc in docs:
        doc_ref = db.collection('weekly_prediction').document(doc.id)
        doc_ref.update({'enabled': False})

    # On Ajoute la nouvelle entrée
    weekly_prediction_ref.add({
        'value': value,
        'enabled': True,
        'created_at': date_time,
    })






