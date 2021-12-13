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



    def __init__(self, scheduler, config, cua, mostrador):
        self.state="inactiu"
        self.scheduler = scheduler
        self.config = config
        self.cua = cua
        self.mostrador = mostrador
        #self.scheduler = Scheduler()


    # generacioPassatgers
    def SimulationStart(self):
        self.ProgramarSeguentArribada()

    # Seguent arribada
    def ProgramarSeguentArribada(self):
        tempsEntreArribades = 1

        #Definim tants mostradors com definit a config.
        for i in range (0, int(self.config.mostradors)):
            mostrador = Mostradors()
            mostradorInicialitzat = Event(self.mostrador, 0, EventType.MOSTRADOR_INICIALITZAT, mostrador)
            self.scheduler.afegirEsdeveniment(mostradorInicialitzat)


        #Creem esdeveniments de canvi de torn
        canvideTorn = Event(self.mostrador, 28800, EventType.CANVI_DE_TORN, None)
        self.scheduler.afegirEsdeveniment(canvideTorn)

        #18:00h
        canvideTorn = Event(self.mostrador, 57600, EventType.CANVI_DE_TORN, None)
        self.scheduler.afegirEsdeveniment(canvideTorn)

        #22:30h
        canvideTorn = Event(self.mostrador, 73800, EventType.CANVI_DE_TORN, None)
        self.scheduler.afegirEsdeveniment(canvideTorn)

        # creem tants passatgers com definit a config i li assignem un temps d'arribada
        for i in range(0, int(self.config.passatgers)):
            passatger = Passatger()
            # posar distribució
            tempsEntreArribades+=60
            self.afegirCua(passatger)
            #TO-DO 10 --> temps a fer la cua
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
