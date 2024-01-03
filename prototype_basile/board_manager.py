

# import des constantes
from constantes.constantes import *
from constantes.dmx_channels import *
from lamp import Lamp
import time
import math


class BoardManager:
    def __init__(self, debug=True) -> None:
        """Gestion des actions faite par la carte"""
        self.debug = debug

        # import des libs
        if self.debug:
            print("debug mode")
            from board_debug import Board
            self.board = Board()
            self.debug_type = "slider"
            self.loop_count = 0
        else:
            self.board = __import__("board")
            import rotaryio
            import analogio
            from lib import math
            from lib import time
            from lib import dmx_transmitter
        
        # PINS
        DMX_PIN = self.board.GP0
        DIM_PIN = (self.board.D9, self.board.D10)
        POS_PIN = (self.board.A1, self.board.A2)


        # Import des entrées/sorties
        # Factice si en mode debug
        if self.debug:
            self.dmx = None
            self.dim_slider = DIM_PIN[0]
            self.js_axe_x, self.js_axe_y = POS_PIN[0], POS_PIN[1]
        # Réels sinon
        else:
            # Instantiation du DMX
            self.dmx = dmx_transmitter.DMXTransmitter(first_out_pin=DMX_PIN)

            # Instantiation des appareils d'inputs
            self.dim_slider = rotaryio.IncrementalEncoder(DIM_PIN[0],DIM_PIN[1])
            self.js_axe_x, self.js_axe_y = analogio.AnalogIn(POS_PIN[0]), analogio.AnalogIn(POS_PIN[1])


        # Création des lampes
        self.lamps = [
            Lamp(LAMPS_POS[0]),
            Lamp(LAMPS_POS[1], DMX_begin=21),
            Lamp(LAMPS_POS[2], DMX_begin=41, reversed=True, reverse_angle=[True, True]),
            Lamp(LAMPS_POS[3], DMX_begin=61, reversed=True, reverse_angle=[True, True])
        ]

        self.selected = 0
        self.pos_x, self.pos_y, self.pos_z  = 250, 0, 100
        

    def range_map(self, x, in_min : int, in_max : int, out_min : int, out_max : int, dmx=False):
        """Renvoie une valeur x comprise entre in_min et in_max re-mappée entre out_min et out_max"""
        if dmx:
            return round((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)
        else:
            return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    def update(self):
        """update les valeurs et le dmx. Envoie des données sur la console si debug = True"""
        if self.debug:
            self.board.update(self.debug_type, self.loop_count)
        
        self.pos_z += self.js_axe_x.value/100
        if self.pos_z > TAILLE_Z:
            self.pos_z = TAILLE_Z
        elif self.pos_z < 0:
            self.pos_z = 0
        
        self.pos_y += self.js_axe_y.value/100
        if self.pos_y > TAILLE_Y:
            self.pos_y = TAILLE_Y
        elif self.pos_y < 0:
            self.pos_y = 0
        

        if not self.selected:
            for lamp in self.lamps:
                lamp.dim = self.dim_slider.value
                lamp.light_pos((self.pos_x, self.pos_y, self.pos_z))
        else:
            self.lamps[self.selected-1].dim = self.dim_slider.value

        
        # Envoi des données, à la console si debug, en DMX sinon 
        if self.debug:
            match self.debug_type:
                case "slider":
                    print(f"dim value : {self.lamps[0].dim} | remapped : {self.range_map(self.lamps[0].dim, 0, 1000, 0, 255, True)}")
                case "js_x":
                    print(f"targeted pos : {self.pos_x}, {self.pos_y}, {self.pos_z} | angles values : θ={round(self.lamps[0].theta/math.pi, 2)}π, Φ={round(self.lamps[0].phi/math.pi, 2)}π | remapped : θ={self.range_map(self.lamps[0].theta, 0-math.pi/2, math.pi/2, 0, 255, True)}, Φ={self.range_map(self.lamps[0].phi, 0, math.pi, 0, 255, True)},")
                case "js_y":
                    print(f"targeted pos : {self.pos_x}, {self.pos_y}, {self.pos_z} | angles values : θ={round(self.lamps[0].theta/math.pi, 2)}π, Φ={round(self.lamps[0].phi/math.pi, 2)}π | remapped : θ={self.range_map(self.lamps[0].theta, 0-math.pi/2, math.pi/2, 0, 255, True)}, Φ={self.range_map(self.lamps[0].phi, 0, math.pi, 0, 255, True)},")
            self.loop_count += 1
        else:
            self.dmx 