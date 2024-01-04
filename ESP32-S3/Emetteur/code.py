import time 
from adafruit_ble_radio import Radio
# Choix du canal de communication
r = Radio(channel=7)
# Conversion du tableau en données binaires
dmx = [255,255,255,0,0,0]
data = bytes(dmx[0:6])
while True:
    time.sleep(1)
    # Envoi des données binaires
    r.send_bytes(data)

