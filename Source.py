from Config import *
from Passatger import *
from random import randint
from Event import *
from Cua import *
from Scheduler import *

class Source:

    state = 0
    index=-1
    tempsArribada = []
    passatgers = []



    def __init__(self, scheduler, config, cua):
        self.state="inactiu"
        self.scheduler = scheduler
        self.config = config
        self.cua = cua
        #self.scheduler = Scheduler()


    # generacioPassatgers
    def SimulationStart(self):
        self.ProgramarSeguentArribada()

    # Seguent arribada
    def ProgramarSeguentArribada(self):
        tempsEntreArribades = 1

        # creem tants passatgers com definit a config i li assignem un temps d'arribada
        for i in range(0, int(self.config.passatgers)):
            passatger = Passatger()
            # posar distribució
            tempsEntreArribades+=1
            self.afegirCua(passatger)
            novaArribada = Event(self.cua, tempsEntreArribades, EventType.ENTRA_A_CUA, passatger)
            self.scheduler.afegirEsdeveniment(novaArribada)
      

    def tractarEsdeveniment(self, event):
        print ("event")
        
    def afegirCua(self, passatger):
        self.cua.cua.append(passatger)
        
    def nextArrival(self):
        global index
        self.index+=1
        

    def name(self):
        return "Generador"

    def changeState(self):
        self.state = (self.state + 1) % 2
