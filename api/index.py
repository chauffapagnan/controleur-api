from fastapi import FastAPI
import asyncio
from api.mqtt_topic import *
from api.mqtt_paho import *

app = FastAPI()
initFirebase()

TIME_OUT = 50


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
    # envoieFireBase(etat)
    # #envoieFireBase(etat)
    # client.loop_stop()
    # client.publish("CONTROL", payload=transcript(etat))
    # client.loop_start()
    return {"etatChauffagee not Saved in DB : ": etat}


@app.post("/creneau/{value}")
async def creneau(value: str):
    envoieFireBase(value)
    return {"creneau not Saved in DB : ": value}


@app.get("/cron")
async def test_cron():
    # Run for 60 seconds
    end_time = asyncio.get_event_loop().time() + TIME_OUT
    while asyncio.get_event_loop().time() < end_time:
        client.loop()
        await asyncio.sleep(TIME_OUT//60)  # Sleep for 1 second

    return {"CRON": "vercel cron"}


@app.post("/cron")
async def test_cron_post():
    # Run for 40 seconds
    end_time = asyncio.get_event_loop().time() + TIME_OUT
    while asyncio.get_event_loop().time() < end_time:
        client.loop()
        await asyncio.sleep(TIME_OUT//60)  # Sleep for this second

    return {"CRON": "test cron QStash"}


# 10h
# 13h
# 16h
# 20h
# Chaque Matin MIDI et SOIR, on va chercher l'état du chauffage (Energie produite, etc)
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_get_energie_produite_from_chauffage")
async def cron_get_energie_produite_from_chauffage():
    client.publish(ENERGY_ASK, payload=1)
    client.loop_write()
    end_time = asyncio.get_event_loop().time() + TIME_OUT-10  # 10 seconde pour le temps du publish
    while asyncio.get_event_loop().time() < end_time:
         client.loop()
         await asyncio.sleep((TIME_OUT-10)//60)  # Sleep for this second

    return {"QStash CRON": "every 10h 13h 16h 20h"}


# 23h
# On va envoyer selon notre calcul la prédiction de l'energie
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_send_daily_prediction_to_app")
async def cron_send_daily_prediction_to_app():
    client.publish(PREDICTION, payload="{'matin': 16, 'midi': 18, 'soir': 15}")
    client.loop_write()
    end_time = asyncio.get_event_loop().time() + TIME_OUT-20  # 10 seconde pour le temps du publish
    while asyncio.get_event_loop().time() < end_time:
         client.loop()
         await asyncio.sleep((TIME_OUT-20)//60)  # Sleep for this second

    return {"QStash CRON Daily prediction": "every 23h"}


