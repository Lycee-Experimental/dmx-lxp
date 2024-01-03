import math

class Lamp:
    def __init__(self, pos : tuple[int, int, int], DMX_begin=1, base_angle=0, reversed=False, reverse_angle=[False,False]) -> None:
        """Objet representant une lumière à tête tournante
        
        Attributs:
        DMX_begin: premier channel DMX attribué à cette lampe. Ce setup utilise ? channels
        
        
        """
        # Caractéristiques de la lampe
        self.max_theta = 720
        self.DMX_begin = DMX_begin # Premier channel utilisé par la lampe
        self.reversed = reversed # Indique si la lampe est montée a l'envers/ a droite du repere
        self.reverse_angle = reverse_angle

        # Position de la lampe dans l'espace
        self.pos_x, self.pos_y, self.pos_z = pos
        
        # Orientation de la tête
        self.theta = 0
        self.phi = 0
        
        # Couleurs
        self.l_R = 0
        self.l_G = 0
        self.l_B = 0
        self.l_W = 0
        self.l_A = 0
        self.l_V = 0

        # Dimmer
        self.dim = 0

    def get_dmx(self) -> list:
        """Retourne une liste contenant les valeurs de tout les channels DMX utilisés par cette lampe. Utiliser self.DMX_begin pour les envoyer correctement"""
        return [self.theta, self.phi, self.dim, self.l_R, self.l_G, self.l_B, self.l_W, self.l_A, self.l_V]
    
    def light_pos(self, target_pos : tuple[int, int, int]) -> None:
        
        # Création du vecteur Lampe -> Cible, inversé si la lampe est de l'autre coté
        target_vector = []
        target_vector.append((-1)**self.reversed * (target_pos[0] - self.pos_x))
        target_vector.append((-1)**self.reversed * (target_pos[1] - self.pos_y))
        target_vector.append((target_pos[2] - self.pos_z))


        self.theta = ((-1)**self.reverse_angle[0]) * math.atan(target_vector[1]/target_vector[0])
        self.phi = ((-1)**self.reverse_angle[1]) * math.acos(target_vector[2]/math.sqrt(target_vector[0]**2+target_vector[1]**2+target_vector[2]**2))