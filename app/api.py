from typing import Union
from fastapi import FastAPI
from models.Controller import Controller
from app.service import *
import asyncio

from app.mqtt_paho import *

app = FastAPI()
initFirebase()

from pydantic import BaseModel

def transcript(etat: bool):
    if etat:
        return 1
    else:
        return 0

@app.get("/")
async def read_root():
    #client.loop_read()
    # client.subscribe("#", qos=1)
    # client.loop_forever()
    return {"chauffage": "Controleur API "}


@app.post("/etat_chauffage/{etat}")
async def update_etat_chauffage(etat: bool):
    envoieFireBase(etat)
    # #envoieFireBase(etat)
    # client.loop_stop()
    # client.publish("CONTROL", payload=transcript(etat))
    # client.loop_start()
    return {"etatChauffagee : ": etat}


@app.get("/cron")
async def test_cron():
    envoieFireBase(True)
    return {"CRON": " every 5 minutes "}


@app.post("/cron")
async def test_cron_post():
    client.loop_stop()
    # Run for 4 seconds
    end_time = asyncio.get_event_loop().time() + 4

    while asyncio.get_event_loop().time() < end_time:
        client.loop_start()
        await asyncio.sleep(1)  # Sleep for 1 second

    return {"CRON": "every 1 minute"}
