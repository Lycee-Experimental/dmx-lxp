"""Reception du message DMX par BLE et transmission via le MOSI du SPI"""
#############
# RADIO BLE #
#############
from adafruit_ble_radio import Radio
# Choix du canal de communication
radio = Radio(channel=7)

##############################
#             DMX            #
##############################

import board
# Définition des pins
SCLK_PIN = board.IO42
MOSI_PIN = board.IO43 # Seul le MOSI doit être connecté, pas besoin du SCLK

# Instanciation du DMX
import dmx
univ = dmx.universe(sck=SCLK_PIN, mosi=MOSI_PIN)

###########################
## Lancement de la boucle #
###########################

import time

while True:
    msg = radio.receive_full()
    if msg:
        data=msg[0]
        # Envoi des données DMX
        univ.send(data)
        time.sleep(0.01)

