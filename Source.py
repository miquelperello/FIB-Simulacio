from Config import *
from Passatger import *
from random import randint
from Event import *
from Cua import *
from Scheduler import *
import numpy as np
import matplotlib.pyplot as plt


class Source:

    state = 0
    index = -1
    tempsArribada = []
    passatgers = []
    # Distribution
    bins = []
    n = []

    def __init__(self, scheduler, config, cua, mostrador):
        self.state = "inactiu"
        self.scheduler = scheduler
        self.config = config
        self.cua = cua
        self.mostrador = mostrador
        self.entitats_creades = 0
        # self.scheduler = Scheduler()

    # generacioPassatgers

    def SimulationStart(self):
        self.GenerateDistribution()
        self.ProgramarSeguentArribada()

    # Seguent arribada

    def ProgramarSeguentArribada(self):

        # Definim tants mostradors com definit a config.
        for i in range(0, max(int(self.config.mostradors1), int(self.config.mostradors2), int(self.config.mostradors3))):
            print("1")
            mostrador = Mostradors()
            mostradorInicialitzat = Event(
                self.mostrador, 0, EventType.MOSTRADOR_INICIALITZAT, mostrador)
            self.scheduler.afegirEsdeveniment(mostradorInicialitzat)

        # Creem esdeveniments de canvi de torn
        canvideTorn = Event(self.mostrador, 28800,
                            EventType.CANVI_DE_TORN, None)
        self.scheduler.afegirEsdeveniment(canvideTorn)

        # 18:00h
        canvideTorn = Event(self.mostrador, 57600,
                            EventType.CANVI_DE_TORN, None)
        self.scheduler.afegirEsdeveniment(canvideTorn)

        # 22:30h
        canvideTorn = Event(self.mostrador, 73800,
                            EventType.CANVI_DE_TORN, None)
        self.scheduler.afegirEsdeveniment(canvideTorn)

        # Distribució
        # Definim temps entre arribades

        tempsEntreArribades = 0
        tempsEntrePersones = 0

        # creem tants passatgers com definit a config i li assignem un temps d'arribada
        comptador = 0
        for i in self.bins:
            tempsEntrePersones = 0
            for j in range(0, int(self.n[comptador])):
                passatger = Passatger()
                tempsEntrePersones += 10
                tempsEntreArribades += int((i-2)*3600)
                tempsEntreArribades += tempsEntrePersones
                tempsEntreArribades = tempsEntreArribades
                passatger.temps_entrada_cua = tempsEntreArribades
                novaArribada = Event(self.cua, tempsEntreArribades,
                                     EventType.ENTRA_A_CUA, passatger)
                self.scheduler.afegirEsdeveniment(novaArribada)
                self.entitats_creades += 1
                tempsEntreArribades = 0
            comptador += 1

        # Creem un esdeveniment de tancament d'aeroport
        Tancament = Event(self.mostrador, 80000,
                          '0', None)
        self.scheduler.afegirEsdeveniment(Tancament)

    def tractarEsdeveniment(self, event):
        print("event")

    def afegirCua(self, passatger):
        self.cua.cua.append(passatger)

    def nextArrival(self):
        global index
        self.index += 1

    def name(self):
        return "Generador"

    def summary(self):
        print('Entitats arribades al sistema: ', self.entitats_creades)

    def changeState(self):
        self.state = (self.state + 1) % 2

    def GenerateDistribution(self):
        X1 = gfg = np.random.triangular(
            2, 10, 16, int(int(self.config.passatgers) / 2))
        X2 = gfg = np.random.triangular(
            12, 17, 22, int(int(self.config.passatgers) / 2))
        X = np.concatenate([X1, X2])

        plt.figure(1)
        (n, bins, patches) = plt.hist(X)
        plt.close(1)

        # From docs: https://matplotlib.org/1.3.1/api/pyplot_api.html#matplotlib.pyplot.hist
        #  If an integer is given, bins + 1 bin edges are returned
        if (len(bins) != len(n)):
            self.bins = bins[:-1]
        else:
            self.bins = bins
        self.n = n
