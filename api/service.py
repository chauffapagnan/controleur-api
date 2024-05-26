import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import calendar
import time
from datetime import datetime
import random

ALLUME = 1
ETEINS = 0
RIEN = None


def initFirebase():
    cred = credentials.Certificate('api/credit.json')
    firebase_admin.initialize_app(cred)


def envoieFireBase(etat):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(time_stamp)
    db = firestore.client()
    db.collection('Controler').add({'date': date_time, 'etat': etat})


def editFireBaseEnabledCreneau():
    db = firestore.client()

    # On Récupère toutes les entrées existantes
    creneau_ref = db.collection('creneau')
    docs = creneau_ref.stream()

    # On Met à jour chaque entrée pour définir enabled à false
    for doc in docs:
        doc_ref = db.collection('creneau').document(doc.id)
        doc_ref.update({'enabled': False})

def envoieFireBaseCreneau(time_string: str):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(time_stamp)

    start_hour, end_hour = time_string.split('-')
    start_hour, start_minute = start_hour.split(':')
    end_hour, end_minute = end_hour.split(':')

    db = firestore.client()

    # On Récupère toutes les entrées existantes
    creneau_ref = db.collection('creneau')
    docs = creneau_ref.stream()

    # On Met à jour chaque entrée pour définir enabled à false
    for doc in docs:
        doc_ref = db.collection('creneau').document(doc.id)
        doc_ref.update({'enabled': False})

    # On Ajoute la nouvelle entrée
    creneau_ref.add({
        'start_hour': start_hour,
        'start_minute': start_minute,
        'end_hour': end_hour,
        'end_minute': end_minute,
        'enabled': True,
        'created_at': date_time,
    })


# une fonction qui va récupérer la donnée parmi la collection creneau dont "enabled = True"
def get_enabled_creneau():
    db = firestore.client()

    # Requête pour récupérer le document avec enabled = True
    creneau_ref = db.collection('creneau')
    query = creneau_ref.where('enabled', '==', True).limit(1)
    results = query.stream()

    # Extraire et retourner le document
    for doc in results:
        return doc.to_dict()

    return None


def check_heating_status():
    # Récupérer le créneau activé
    creneau = get_enabled_creneau()

    if creneau:
        # Récupérer l'heure et la minute actuelle
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # Récupérer les heures et minutes de début et de fin du créneau
        start_hour = int(creneau['start_hour'])
        start_minute = int(creneau['start_minute'])
        end_hour = int(creneau['end_hour'])
        end_minute = int(creneau['end_minute'])

        # Comparer les heures et minutes
        if current_hour == start_hour:
            if current_minute >= start_minute:
                print("Chauffage allume toi !")
                return ALLUME
            else:
                print("On ne fait rien")
                return RIEN

        if current_hour == end_hour:
            if current_minute >= end_minute:
                print("Chauffage éteins toi !")
                return ETEINS
            else:
                print("On ne fait rien")
                return ALLUME

        if current_hour > start_hour and current_hour < end_hour:
            print("Chauffage allume toi !")
            return ALLUME

        if current_hour < start_hour:
            print("On ne fait rien")
            return RIEN
        if current_hour > end_hour:
            print("Chauffage éteins toi !")
            return ETEINS

    else:
        print("Aucun créneau activé trouvé.")
        return RIEN


def envoieFireBaseEnergieProduite(energie):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(time_stamp)
    db = firestore.client()
    db.collection('energie_produite').add({'date': date_time, 'value': energie})



    
