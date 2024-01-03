"""
Exemple de controleur DMX à 2 canaux avec un RP2040.
Un joysticks change les valeurs des canaux.
Un encodeur rotatif permet de choisir le preset dans lequel enregistrer les valeurs des canaux.
"""
######################################
# Définition des Pins GPIO utilisées #
######################################

import board # Pour accéder aux GPIO

DMX_PIN = board.GP0 # On pilote le module RS485 avec GP0
JOY_X_PIN = board.A0 # L'axe X du Joystick
JOY_Y_PIN = board.A1 # L'axe Y du joystick
ENC_1 = board.GP1 # Pin 1 de l'encodeur rotatif
ENC_2 = board.GP2 # Pin 2 de l'encodeur rotatif
ENC_BTN = board.GP3 # Bouton de l'encodeur rotatif
SCREEN_SCL=board.GP5 # SCL de l'écran
SCREEN_SDA=board.GP4 # SDA de l'écran
######################################
#        Instanciation du DMX        #
######################################

from dmx_transmitter import dmx_transmitter # Uniquement pour les RP2040 : à télécharger depuis https://github.com/mydana/CircuitPython_DMX_Transmitter
dmx = dmx_transmitter.DMXTransmitter(first_out_pin=DMX_PIN)

######################################
#      Configuration du Joystick     #
######################################

import analogio
ax = analogio.AnalogIn(JOY_X_PIN)
ay = analogio.AnalogIn(JOY_Y_PIN)

def range_map(x, in_min, in_max, out_min, out_max):
    """"Répartit les valeurs prises par le joystick sur une échelle de -127 à 127"""
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


######################################
# Configuration de l'encodeur rotatif#
######################################

import rotaryio # pour l'encodeur rotatif
import digitalio # pour le bouton

encoder = rotaryio.IncrementalEncoder(ENC_1, ENC_2)
button = digitalio.DigitalInOut(ENC_BTN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
button_state = None
last_position = encoder.position
preset = 1

######################################
#        Mémoire non volatile        #
#   pour enregistrer les presets     #
######################################

import microcontroller
#microcontroller.nvm[0:3] = b"\xcc\x10\x00"


######################################
#    Affichage sur écran SSD1306     #
######################################
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label

# On efface le contenu de l'écran
displayio.release_displays()
# On déclare un port I2C sur les pins GP0 et GP0
i2c = busio.I2C(scl=SCREEN_SCL, sda=SCREEN_SDA)
# On déclare le bus de notre écran à l'adresse 0x3C
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
# On déclare notre ssd1306 de 128x32 pixels sur le bus précédent
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
text_group = displayio.Group()
text_area = label.Label(terminalio.FONT, text="Preset 1", color=0xFFFFFF, x=0, y=8, scale=2)
text_group.append(text_area)
text_area = label.Label(terminalio.FONT, text="En cours d'édition...", color=0xFFFFFF, x=0, y=25)
text_group.append(text_area)
display.show(text_group)

######################################
#       Lancement de la boucle       #
######################################
import time # Pour les sleep

while True:
    

    # Mouvements du Joysticks sur les canaux DMX 0 et 1
    dx=range_map(ax.value, 0, 4095, -127, 127)
    dy=range_map(ay.value, 0, 4095, -127, 127)
    if dx !=0:
        val = dmx[0] + dx
        dmx[0] = 0 if val < 0 else (255 if val > 255 else val)
    if dy !=0:
        val = dmx[1] + dy
        dmx[1] = 0 if val < 0 else (255 if val > 255 else val)

    # Mouvements de l'encodeur pour choisir un preset
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change:
        preset = 1 if (preset + position_change) <= 1 else preset + position_change
        # On modifie le texte affiché sur l'écran
        text_group = displayio.Group()
        text_area = label.Label(terminalio.FONT, text=f"Preset {preset}", color=0xFFFFFF, x=0, y=8, scale=2)
        text_group.append(text_area)
        text_area = label.Label(terminalio.FONT, text="En cours d'édition...", color=0xFFFFFF, x=0, y=25)
        text_group.append(text_area)
        display.show(text_group)
        last_position = current_position
    # Bouton appuyé
    if not button.value and button_state is None:
        button_state = "pressed"
    # Bouton relâché
    if button.value and button_state == "pressed":
        # On enregistre le preset dans la mémoire non volatile (NVM)
        microcontroller.nvm[preset*2-2:preset*2] = dmx[0:2]
        # On modifie le texte affiché sur l'écran
        text_group = displayio.Group()
        text_area = label.Label(terminalio.FONT, text=f"Preset {preset}", color=0xFFFFFF, x=0, y=8, scale=2)
        text_group.append(text_area)
        text_area = label.Label(terminalio.FONT, text="Enregistré", color=0xFFFFFF, x=0, y=25)
        text_group.append(text_area)
        display.show(text_group)
        button_state = None


    # On envoie les nouvelles valeurs aux lampes
    dmx.show()
    # On attends 1/10 s avant de recommencer
    time.sleep(0.1)


