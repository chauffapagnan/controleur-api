from dotenv import load_dotenv
import os 
import uvicorn
from app.mqtt_paho import *
import threading

load_dotenv()
PORT = int(os.get('PORT', 8000))
HOST = '0.0.0.0'

if __name__ == '__main__':
    # Start MQTT client in a separate thread
    mqtt_thread = threading.Thread(target=startMQTT)
    mqtt_thread.start()

    # Start Uvicorn server
    uvicorn.run('app.api:app', host=HOST, port=PORT, reload=True)
