import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import calendar
import time
from datetime import datetime
import random

def envoieFireBase(etat):   
    cred = credentials.Certificate('app/credit.json')
    firebase_admin.initialize_app(cred)

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(time_stamp)
    db=firestore.client()
    db.collection('Controler').add({'date':date_time,'etat':etat})
 

    
