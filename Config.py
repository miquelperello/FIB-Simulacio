

import Scheduler
from Mostradors import *


class Config:

    mostradors = "None"
    treballadors = "None"
    passatgers = "None"


    def __init__(self):
        self.state="inactiu"
        

    def configurarModel(self):
        global mostradors, treballadors, passatgers
        print("# Comença la configuració")
        Config.mostradors = input("Quin número de mostradors vols estudiar? ")
        Config.treballadors = input(f"Quants treballadors vols per mostrador? ")
        Config.passatgers = input(f"Quants passatgers? ")        
        print("\n")
        


    def printTreballadors(self, num):
        global treballadors
        self.treballadors = num
        print("inside print" + str(self.treballadors))
        return self.treballadors
    
    
    def printMostradors(self):
        global mostradors
        print("inside print" + str(self.mostradors))
        return self.mostradors
