

import Scheduler
from Mostradors import *
from datetime import *

class Config:

    mostradors = "None"
    treballadors = "None"
    passatgers = "None"
    veuretraza = "None"


    def __init__(self):
        self.state="inactiu"
        

    def configurarModel(self):
        global mostradors, treballadors, passatgers
        print("# Comença la configuració")
        #Config.mostradors = input("Quin número de mostradors vols estudiar? ")
        Config.mostradors = 20
        Config.treballadors = input(f"Quants treballadors vols per mostrador? ")
        Config.passatgers = input(f"Quants passatgers? ")
        Config.veuretraza = input(f"Vols veure traza? 1 Sí, 0 No ")
        print("\n")
        




    def returnMostradors(self,tid):
        #Segons el temps retornem el num de Mostradors disponibles
        temps1 = datetime.strptime("01/01/21 10:00", "%d/%m/%y %H:%M")
        temps2 = datetime.strptime("01/01/21 18:00", "%d/%m/%y %H:%M")
        temps3 = datetime.strptime("01/01/21 22:30", "%d/%m/%y %H:%M")

        tempsInicial = datetime.strptime("01/01/21 02:00", "%d/%m/%y %H:%M")
        tempsFinal = tempsInicial + datetime(tid)

        if(((tempsFinal < temps1) or ((tempsFinal > temps2) and (tempsFinal < temps3)))):
            return 6
        return 4


    def printTreballadors(self, num):
        global treballadors
        self.treballadors = num
        print("inside print" + str(self.treballadors))
        return self.treballadors
    
    
    def printMostradors(self):
        global mostradors
        print("inside print" + str(self.mostradors))
        return self.mostradors
