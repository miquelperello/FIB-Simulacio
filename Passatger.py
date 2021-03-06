from random import randint
from auxiliar import *
import numpy as np


class Passatger:
    id = ""
    maleta = ""
    documentacio = ""
    temps = ""
    mostrador_assignat = ""
    perd_avio = ""

    def __init__(self, temps=None):

        global id
        if (temps == None):
            self.id = randint(0, 10000)
            self.estat = State.ACTIVE
            self.maleta = int(np.random.triangular(0, 1, 4))
            self.temps = 0
            self.mostrador_assignat = -1
            self.perd_avio = 0

            self.temps_entrada_cua = 0
            self.temps_entrada_mostrador = 0
            self.temps_sortida_mostrador = 0
        else:
            self.id = randint(0, 10000)
            self.estat = State.ACTIVE
            self.maleta = randint(0, 4)
            self.temps = str(temps)
            self.mostrador_assignat = -1

            self.temps_entrada_cua = 0
            self.temps_entrada_mostrador = 0
            self.temps_sortida_mostrador = 0
            self.perd_avio = 0
