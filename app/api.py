from typing import Union
from fastapi import FastAPI
from models.Controller import Controller
from app.service import *
from app.mqtt_paho import *

app = FastAPI()

from pydantic import BaseModel

def transcript(etat: bool):
    if etat:
        return 1
    else:
        return 0

@app.get("/")
async def read_root():
    client.loop_stop()
    client.loop_start()
    return {"chauffage": "Controleur API "}

@app.post("/etat_chauffage/{etat}")
async def update_etat_chauffage(etat: bool):
    #envoieFireBase(etat)
    client.loop_stop()
    client.publish("CONTROL", payload=transcript(etat))
    client.loop_start()
    return {"etatChauffagee : ": etat}
    
