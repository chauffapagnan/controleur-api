import time
import paho.mqtt.client as paho
from paho import mqtt
from api.service import *
from api.mqtt_config import *


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("[MQTT-OK] CONNECT received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None, payload=None):
    print("[MQTT-OK] publish mid : " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("[MQTT-OK] Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    if msg.topic == ENERGY_RESP:
        envoieFireBaseEnergieProduite(str(msg.payload))
    elif msg.topic == ACK:  # le ONOFF
        envoieFireBase(str(msg.payload))

    print("[MQTT- on message] " + "Topic : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(paho.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(mqtt_host_username, mqtt_host_password)

# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(mqtt_host_name, mqtt_host_port)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("#", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop