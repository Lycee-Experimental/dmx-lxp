"""Reception de signal BLE et transmission via le MOSI du SPI"""
#############
# RADIO BLE #
#############

import adafruit_ble_radio
from adafruit_ble_radio import Radio
# Obtenir 512 canaux (defaut 248)
adafruit_ble_radio.MAX_LENGTH = 512 
# Choix du canal de communication
radio = Radio(channel=7)

##############################
# Utilisation du MOSI du SPI #
##############################

import board

# Définition des pins
SCLK_PIN = board.IO42
MOSI_PIN = board.IO9 # Seul le MOSI doit être connecté, pas besoin du SCLK

# Déclaration du SPI
import dmx
univ = dmx.universe(sck=SCLK_PIN, mosi=MOSI_PIN)

###########################
## Lancement de la boucle #
###########################

# Nécessaire de lancer une fonction main avec asyncio pour lancer la tache send_dmx de la librairie dmx
import asyncio   

async def main():
    while True:
        # Timeout nécessaire (par défaut 1s) pour ne pas couper send_dmx trop longtemps
        msg = radio.receive_full(timeout=0.1)
        if msg:
            # Envoi des données DMX
            univ.change_data(msg[0])
        # Redonne le contrôle à la tache async send_dmx
        await asyncio.sleep(0) 

asyncio.run(main())
