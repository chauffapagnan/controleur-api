from fastapi import FastAPI
import asyncio
# from api.mqtt_config import *
from api.mqtt_paho import *
# from api.prediction.meteo_weekly import *
# from api.prediction.RandomForest_energy_prediction import *

app = FastAPI()
initFirebase()

TIME_OUT = 50

def transcript(etat: bool):
    if etat:
        return 1
    else:
        return 0

a = 3


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

@app.get("/get_creneau")
async def creneau(value: str):
    return get_enabled_creneau()


@app.get("/cron")
async def test_cron():
    try:
        client.connect(mqtt_host_name, mqtt_host_port)
        # Run for 60 seconds
        end_time = asyncio.get_event_loop().time() + TIME_OUT
        while asyncio.get_event_loop().time() < end_time:
            client.loop()
            await asyncio.sleep(TIME_OUT//60)  # Sleep for 1 second
        client.disconnect()

    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
        pass
    return {"CRON": "vercel cron"}


@app.post("/cron")
async def test_cron_post():
    try:
        client.connect(mqtt_host_name, mqtt_host_port)
        # Run for 40 seconds
        end_time = asyncio.get_event_loop().time() + TIME_OUT
        while asyncio.get_event_loop().time() < end_time:
            client.loop()
            await asyncio.sleep(TIME_OUT//60)  # Sleep for this second
        client.disconnect()

    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
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
        # Connect to MQTT broker
        client.connect(mqtt_host_name, mqtt_host_port)
        client.publish(ENERGY_ASK, payload=1)
        end_time = asyncio.get_event_loop().time() + TIME_OUT-20  # 10 seconde pour le temps du publish
        while asyncio.get_event_loop().time() < end_time:
             client.loop()
             await asyncio.sleep((TIME_OUT-20)//60)  # Sleep for this second

        client.disconnect()

    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
        pass

    return {"QStash CRON": "every 10h 13h 16h 20h"}


static_pred = "{'Lundi': 19.89, 'Mardi': 19.616666666666664, 'Mercredi': 19.556666666666665, 'Jeudi': 18.33, 'Vendredi': 18.49, 'Samedi': 18.49, 'Dimanche': 19.91}"
# 23h
# On va envoyer selon notre calcul la prédiction de l'energie
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_send_daily_prediction_to_app")
async def cron_send_daily_prediction_to_app():
    try:
        # Connect to MQTT broker
        client.connect(mqtt_host_name, mqtt_host_port)
        client.publish(PREDICTION, payload=get_weekly_prediction())
        end_time = asyncio.get_event_loop().time() + TIME_OUT-20  # 10 seconde pour le temps du publish
        while asyncio.get_event_loop().time() < end_time:
             client.loop()
             await asyncio.sleep((TIME_OUT-20)//60)  # Sleep for this second

        # Disconnect from MQTT broker
        client.disconnect()

    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
        pass
    return {"QStash CRON Daily prediction": "every 23h"}


# chaque 10 minute
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_routine_allumage_with_creneau")
async def cron_routine_allumage_with_creneau():

    try:
        check_time = check_heating_status()
        if check_time == RIEN:
            pass
        else:
            client.connect(mqtt_host_name, mqtt_host_port)
            if check_time == ALLUME:
                client.publish(ONOFF, payload=1)  # on active le Chauffage
                editFireBaseEnabledCreneauStart()  # On met à False enabled du creneau

            elif check_time == ETEINS:
                client.publish(ONOFF, payload=0)  # on éteint le Chauffage
                editFireBaseEnabledCreneauEnd()  # On met à False enabled du creneau

            # client.loop_write()
            end_time = asyncio.get_event_loop().time() + TIME_OUT-30  # 30 seconde pour le temps du publish
            while asyncio.get_event_loop().time() < end_time:
                client.loop()
                await asyncio.sleep((TIME_OUT-30)//60)  # Sleep for this second

            client.disconnect()


    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
        pass

    return {"QStash CRON Routine allumage": "every 10 minutes"}


# 22h chaque Weekend
# @app.post("/cron_meteo_week")
# async def cron_meteo_week():
#     fetch_and_filter_meteo_data()
#     return "Donnée Meteo Week OKay updated"
#
# ## App mobile l'appel
# @app.get("/get_prediction")
# async def get_prediction():
#     print("Making ML Computing")
#     return ML_modeling()


@app.get("/get_prediction")
async def get_prediction():
    return get_weekly_prediction()






"""
"""
"""
"""
"""
"""
"""
"""
"""
""" ## LA PARTIE DE TEST
"""
"""
"""
"""
"""
"""
"""
"""


@app.get("/_test")
async def read_root_test():

    #client.loop_read()
    # client.subscribe("#", qos=1)
    # client.loop_forever()
    return {"chauffage": "Controleur API "}


@app.post("/creneau_test/{value}")
async def creneau_test(value: str):
    return {"creneau Saved in DB : ": value}


@app.get("/cron_test")
async def test_cron_test():
    try :
        # Run for 60 seconds
        end_time = asyncio.get_event_loop().time() + TIME_OUT
        while asyncio.get_event_loop().time() < end_time:
            client.loop()
            await asyncio.sleep(TIME_OUT//60)  # Sleep for 1 second

    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
        pass
    return {"CRON": "vercel cron"}


@app.post("/cron_test")
async def test_cron_post_test():
    try:
        # Run for 40 seconds
        end_time = asyncio.get_event_loop().time() + TIME_OUT
        while asyncio.get_event_loop().time() < end_time:
            client.loop()
            await asyncio.sleep(TIME_OUT//60)  # Sleep for this second

    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
        pass

    return {"CRON": "test cron QStash"}


# 10h
# 13h
# 16h
# 20h
# Chaque Matin MIDI et SOIR, on va chercher l'état du chauffage (Energie produite, etc)
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_get_energie_produite_from_chauffage_test")
async def cron_get_energie_produite_from_chauffage_test():
    try:
        # Connect to MQTT broker
        client.connect(mqtt_host_name, mqtt_host_port)
        client.publish(ENERGY_ASK, payload=1)
        end_time = asyncio.get_event_loop().time() + TIME_OUT-20  # 10 seconde pour le temps du publish
        while asyncio.get_event_loop().time() < end_time:
            client.loop()
            await asyncio.sleep((TIME_OUT-20)//60)  # Sleep for this second

        client.disconnect()

    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
        pass

    return {"QStash CRON": "every 10h 13h 16h 20h"}


# 23h
# On va envoyer selon notre calcul la prédiction de l'energie
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_send_daily_prediction_to_app_test")
async def cron_send_daily_prediction_to_app_test():
    try:
        # Connect to MQTT broker
        client.connect(mqtt_host_name, mqtt_host_port)
        client.publish(PREDICTION, payload=static_pred)
        end_time = asyncio.get_event_loop().time() + TIME_OUT-20  # 10 seconde pour le temps du publish
        while asyncio.get_event_loop().time() < end_time:
            client.loop()
            await asyncio.sleep((TIME_OUT-20)//60)  # Sleep for this second

        # Disconnect from MQTT broker
        client.disconnect()

    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
        pass
    return {"QStash CRON Daily prediction": "every 23h"}


# chaque 10 minute
# Le cron est géré par notre service QStash en ligne
@app.post("/cron_routine_allumage_with_creneau_test")
async def cron_routine_allumage_with_creneau_test():

    try:
        check_time = check_heating_status()
        if check_time == RIEN:
            pass
        else:
            client.connect(mqtt_host_name, mqtt_host_port)
            if check_time == ALLUME:
                client.publish(ONOFF, payload=1)  # on active le Chauffage
                editFireBaseEnabledCreneauStart()  # On met à False enabled du creneau

            elif check_time == ETEINS:
                client.publish(ONOFF, payload=0)  # on éteint le Chauffage
                editFireBaseEnabledCreneauEnd()  # On met à False enabled du creneau

            # client.loop_write()
            end_time = asyncio.get_event_loop().time() + TIME_OUT-30  # 10 seconde pour le temps du publish
            while asyncio.get_event_loop().time() < end_time:
                client.loop()
                await asyncio.sleep((TIME_OUT-30)//60)  # Sleep for this second

            client.disconnect()

    except Exception as e:
        print(f"WRONG : Quelque chose s'est mal passé - {e}")
        pass

    return {"QStash CRON Routine allumage": "every 10 minutes"}


@app.get("/get_prediction_test")
async def get_prediction_test():
    return static_pred











