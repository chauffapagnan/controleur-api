
mqtt_host_name = "3f68ce49b7714ea2ac988e755d35fd99.s1.eu.hivemq.cloud"
mqtt_host_username = "controlleur"
mqtt_host_password = "Controlleur24"
mqtt_host_port = 8883


# Pour activer/désactiver le chauffage depuis le chauffage
ACK = "CONTROL/ACK"
# Pour activer/désactiver le chauffage
ONOFF ="CONTROL/ONOFF"

# Pour demander d’envoyer l’énergie produite à 10h - 13h - 16h - 20h
ENERGY_ASK = "DATA/ENERGY/ASK"
# Pour envoyer l’énergie produite à 10h - 13h - 16h - 20h
ENERGY_RESP = "DATA/ENERGY/RESP"

# Pour envoyer la daily prediction à l’app mobile
PREDICTION = "DATA/PREDICTION"