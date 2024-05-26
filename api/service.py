import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import calendar
import time
from datetime import datetime
import random


def initFirebase():
    cred = credentials.Certificate('api/credit.json')
    firebase_admin.initialize_app(cred)

def envoieFireBase(etat):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(time_stamp)
    db = firestore.client()
    db.collection('Controler').add({'date': date_time, 'etat': etat})


def envoieFireBaseCreneau(time_string: str):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(time_stamp)

    start_hour, end_hour = time_string.split('-')
    start_hour, start_minute = start_hour.split(':')
    end_hour, end_minute = end_hour.split(':')

    db = firestore.client()
    db.collection('creneau').add({
        'start_hour': start_hour,
        'start_minute': start_hour,
        'end_hour': end_hour,
        'end_minute': end_hour,
        'enabled': True,
        'created_at': date_time,
    })

def envoieFireBaseEnergieProduite(energie):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(time_stamp)
    db = firestore.client()
    db.collection('energie_produite_from_chauffage').add({'date': date_time, 'value': energie})



    
