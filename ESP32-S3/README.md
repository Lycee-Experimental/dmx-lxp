# Contrôleur DMX sans fil avec ESP32

## L'ESP32-S3
Les boards ESP32-S3 présente l'avantage à moindre côut (~6€) de présenter de nombreux GPIO, pas mal de mémoire, et surtout la gestion du Bluetooth (BLE) et wifi.

Toutefois la librairie [CircuitPython_DMX_Transmitter](https://github.com/mydana/CircuitPython_DMX_Transmitter) n'est utilisable qu'avec le RP2040 du Raspberry Pico, qui ne gère pas le protocole BLE.

Il est donc nécessaire de réaliser nous-même la communication avec le protocole DMX512. Nous le ferons sur le pin MOSI du protocole SPI.

La librairie `dmx.py` est construite pour cela.


## Protocole DMX512

### Principe

Les communication DMX512 doit s'effectuer à un **baudrate** de 250 kbit/s, soit un bit toute les 4 μs.


```
Idle  |       Break       |MAB|  Slot 0  |  Slot 1  |
------\                   /---\        /-\ /--------\
      |                   |   |        | | |        |
      |                   |   |        | | |        |
      \-------------------/   \--------/ \-/        \-- - -
```


**Idle** : En l'absence de signal, la sortie digitale est à `1` .

**Break** : POur prévenir l'arrivée du signal, il faut commencer par envoyer un signal à ``0`` pendant environ **92 μs**.

**MAB** : Le Mark After Break (MAB) est un signal de **12 μs** à `1` qui suit le **break**.

**Slots** : Les slots correspondent a un signal de départ Slot 0 (un octet à `0`), suivi des octets qui correspondent au valeurs de chaque canaux DMX (512 au maximum). 

Chaque octet doit être précédé d'un bit start à `0` (S), et de 2 stops à `1` (E).

Exemple d'un slot à une valeur de 152 (`0b10011000`).

```
 S 0 1 2 3 4 5 6 7 E E
\ /-\   /---\      /--
| | |   |   |      |
| | |   |   |      |
\-/ \---/   \------/
```

### Utilisation de la librairie dmx.py

```python
import dmx
import board

# Définition des pins
SCLK_PIN = board.IO42
MOSI_PIN = board.IO43 # Le MOSI doit être connecté au MAX485, pas besoin du SCLK...

# Instanciation du DMX
univ = dmx.universe(sck=SCLK_PIN, mosi=MOSI_PIN)

# Envoi de message
msg = b'\x06\x06\x06\x06\x06\x06\x06\x06\x06'    
univ.send(msg)
```

## Transmission des commandes par bluetooth

Avec les modules ESP32, il nous est possible de réaliser un panneau de commande sans fils.

Notre panneau de contrôle contiendra un ESP32 **émetteur**, l'ESP32 **récepteur** ne fera que recevoir les signaux DMX et les transmettre au MAX485.

### Librairie ble_radio

Cette librairie permet de recevoir et transmettre des données

#### Installation

```bash
circup install adafruit_ble_radio
```
#### Utilisation

##### Emission
```python
# Import de la librairie
from adafruit_ble_radio import Radio
# Choix du canal de communication
r = Radio(channel=7)
# Canaux DMX
dmx = [255,255,255,0,0,0]
# Conversion du tableau en données binaires
data = bytes(dmx[0:6])
# Envoi des données binaires
r.send_bytes(data)
```

##### Réception

```python
# Import de la librairie
from adafruit_ble_radio import Radio
# Choix du canal de communication
radio = Radio(channel=7)
while True:
    msg = radio.receive_full()
    if msg:
        data=msg[0]
        print(data)
```