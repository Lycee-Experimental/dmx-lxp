"""
a
"""

import argparse

# Parsing des arguments pour le debugging

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Use debug mode.')

args = parser.parse_args()
debug = args.debug

if debug: print("Mode debug activé")
    


# import des libs
if debug:
    import time
    import math
else:
    import board
    import rotaryio
    import analogio
    from lib import math
    from lib import time
    from lib import dmx_transmitter


# import des fichiers tiers
from board_manager import *

# import des constantes
from constantes.constantes import *
from constantes.dmx_channels import *

board_manager = BoardManager(debug=debug)

running = True
loop_count = 0

while running:
    
    board_manager.update()
    time.sleep(TICK)
    if loop_count%100==0:
        print(f"Boucle n°{loop_count}")
    loop_count+=1
