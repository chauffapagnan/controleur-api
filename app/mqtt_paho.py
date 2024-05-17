import time
import paho.mqtt.client as paho
from paho import mqtt
import threading

# Callbacks for different events
def on_connect(client, userdata, flags, rc, properties=None):
    print("[HIVE MQTT] CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None, payload=None):
    print("[HIVE MQTT] mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("[HIVE MQTT] Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print("[HIVE MQTT] on message " + " topic : " + msg.topic + "  | qos : " + str(msg.qos) + " | msg : " + str(msg.payload))

def mqtt_client_thread():
    # MQTT client setup
    client = paho.Client(paho.CallbackAPIVersion.V5)
    client.on_connect = on_connect


    # Enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # Set username and password
    client.username_pw_set("controlleur", "Controlleur24")
    # Connect to HiveMQ Cloud on port 8883
    client.connect("3f68ce49b7714ea2ac988e755d35fd99.s1.eu.hivemq.cloud", 8883)
    print("[HIVE MQTT] connected to server succeed")

    # Set callbacks
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    # Subscribe to all topics
    client.subscribe("#", qos=1)
    # a single publish, this can also be done in loops, etc.
    client.publish("encyclopedia/temperature", payload="hot", qos=1)

    # Start the loop
    client.loop_forever()

def startMQTT():
    print("[HIVE MQTT] is Starting")
    # Create a thread for the MQTT client
    mqtt_thread = threading.Thread(target=mqtt_client_thread)
    # Start the thread
    mqtt_thread.start()

# Example of starting the MQTT client asynchronously
if __name__ == "__main__":
    startMQTT()
