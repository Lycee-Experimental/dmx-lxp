# Gestion de la radio BLE

import adafruit_ble_radio
from adafruit_ble_radio import Radio
# Ne pas monopoliser les ressources trop longtemps en asyncio (defaut 0.5)
adafruit_ble_radio.AD_DURATION = 0.1 
# Obtenir 512 canaux (defaut 248)
adafruit_ble_radio.MAX_LENGTH = 512 
# Choix du canal de communication
r = Radio(channel=7)



while True:
    user_input = input("Entrer des valeurs de canal dmx (entre 0 et 255) séparées par des virgules : ")
    input_values = user_input.split(',')
    values = []
    for value in input_values:
        try:
            int_value = int(value.strip())
            if 0 <= int_value <= 255:
                values.append(int_value)
            else:
                print(f"Valeurs impossibles: {int_value}. Les valeurs doivent être entre 0 and 255.")
        except ValueError:
            print(f"Valeurs impossibles: {value}. Les valeurs doivent être des entiers.")
    r.send_bytes(bytes(values))

