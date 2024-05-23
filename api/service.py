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
    db=firestore.client()
    db.collection('Controler').add({'date':date_time,'etat':etat})
 

    
