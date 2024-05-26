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
    envoieFireBaseCreneau(value)
    return {"creneau Saved in DB : ": value}


@app.get("/cron")
async def test_cron():
    try :
        # Run for 60 seconds
        end_time = asyncio.get_event_loop().time() + TIME_OUT
        while asyncio.get_event_loop().time() < end_time:
            client.loop()
            await asyncio.sleep(TIME_OUT//60)  # Sleep for 1 second

    except:
        print("WRONG : Quelque chose s'est mal passé")
        pass
    return {"CRON": "vercel cron"}


@app.post("/cron")
async def test_cron_post():
    try:
        # Run for 40 seconds
        end_time = asyncio.get_event_loop().time() + TIME_OUT
        while asyncio.get_event_loop().time() < end_time:
            client.loop()
            await asyncio.sleep(TIME_OUT//60)  # Sleep for this second

    except:
        print("WRONG : Quelque chose s'est mal passé")
        pass

    return {"CRON": "test cron QStash"}


# 10h
# 13h
# 16h
# 20h
# Chaque Matin MIDI et SOIR, on va chercher l'état du chauffage (Energie produite, etc)
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_get_energie_produite_from_chauffage")
async def cron_get_energie_produite_from_chauffage():
    try:
        client.publish("DATA/ENERGY/ASK", payload=1)
        client.loop_write()
        end_time = asyncio.get_event_loop().time() + TIME_OUT-20  # 10 seconde pour le temps du publish
        while asyncio.get_event_loop().time() < end_time:
             client.loop()
             await asyncio.sleep((TIME_OUT-20)//60)  # Sleep for this second

    except:
        print("WRONG : Quelque chose s'est mal passé")
        pass

    return {"QStash CRON": "every 10h 13h 16h 20h"}


# 23h
# On va envoyer selon notre calcul la prédiction de l'energie
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_send_daily_prediction_to_app")
async def cron_send_daily_prediction_to_app():
    try:
        client.publish("DATA/PREDICTION", payload="{'matin': 16, 'midi': 18, 'soir': 15}")
        client.loop_write()
        end_time = asyncio.get_event_loop().time() + TIME_OUT-20  # 10 seconde pour le temps du publish
        while asyncio.get_event_loop().time() < end_time:
             client.loop()
             await asyncio.sleep((TIME_OUT-20)//60)  # Sleep for this second

    except:
        print("WRONG : Quelque chose s'est mal passé")
        pass
    return {"QStash CRON Daily prediction": "every 23h"}


# chaque 10 minute
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_routine_allumage_with_creneau")
async def cron_routine_allumage_with_creneau():

    try:
        if check_heating_status() == (False, False):
            pass
        else:
            if check_heating_status() == (True, False):
                client.publish("CONTROL/ONOFF", payload=1)  # on active le Chauffage

            elif check_heating_status() == (False, True):
                client.publish("CONTROL/ONOFF", payload=0)  # on éteint le Chauffage

            client.loop_write()
            end_time = asyncio.get_event_loop().time() + TIME_OUT-20  # 10 seconde pour le temps du publish
            while asyncio.get_event_loop().time() < end_time:
                client.loop()
                await asyncio.sleep((TIME_OUT-20)//60)  # Sleep for this second

    except:
        print("WRONG : Quelque chose s'est mal passé")
        pass

    return {"QStash CRON Routine allumage": "every 10 minutes"}


