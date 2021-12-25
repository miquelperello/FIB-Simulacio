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

    def __init__(self):
        self.state = "inactiu"
        self.entitats_creades = 0

    def connecta(self, scheduler, config, cua, mostrador):
        self.scheduler = scheduler
        self.config = config
        self.cua = cua
        self.mostrador = mostrador

    def SimulationStart(self):
        self.GenerateDistribution()
        self.ProgramarSeguentArribada()

    # Seguent arribada
    def ProgramarSeguentArribada(self):

        # Definim mostradors
        self.inicialitzaMostradors()

        # Definim canvis de torn i tancament d'aeroport
        self.events_canvi_torn()

        # Definim creació d'arribades
        self.tempsEntreArribades()

    def inicialitzaMostradors(self):
        # Definim tants mostradors com definit a config.
        for i in range(0, max(int(self.config.mostradors1), int(self.config.mostradors2), int(self.config.mostradors3))):
            mostrador = Mostradors()
            mostradorInicialitzat = Event(
                self.mostrador, 0, EventType.MOSTRADOR_INICIALITZAT, mostrador)
            self.scheduler.afegirEsdeveniment(mostradorInicialitzat)

    def events_canvi_torn(self):
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

        # Creem un esdeveniment de tancament d'aeroport
        Tancament = Event(self.mostrador, 80000,
                          EventType.SimulationEnd, None)
        self.scheduler.afegirEsdeveniment(Tancament)

    def tempsEntreArribades(self):
        # Definim temps entre arribades

        tempsEntreArribades = 0
        tempsEntrePersones = 0

        # Creem esdeveniments de creació de passatgers
        for i in range(0, len(self.bins)):
            # Si en el torn hi ha passatgers
            if (int(self.n[i]) > 0):
                EventNovaArribada = Event(self, int((self.bins[i]-2)*3600),
                                          EventType.NOVA_ARRIBADA, i)
                self.scheduler.afegirEsdeveniment(EventNovaArribada)

    def ProgramaNovesArribades(self, comptador):
        tempsEntrePersones = 0
        tempsEntreArribades = 0
        for j in range(0, int(self.n[comptador])):
            passatger = Passatger()
            # Definim un interval de 10 segons entre les persones
            tempsEntrePersones += 10
            # creem tants passatgers com definit i li assignem un temps d'arribada
            # A self.bins[x] trobem l'hora d'arribada i a self.n[x] el nombre de passatgers que arriben a aquella hora.
            # A la variable <<self.bins[comptador]>> trobem la hora d'arribada. Li restem 2 ja que definim el moment 0 com les 2:00h del matí.
            tempsEntreArribades += int((self.bins[comptador]-2)*3600)
            tempsEntreArribades += tempsEntrePersones
            tempsEntreArribades = tempsEntreArribades
            passatger.temps_entrada_cua = tempsEntreArribades
            novaArribada = Event(self.cua, tempsEntreArribades,
                                 EventType.ENTRA_A_CUA, passatger)
            self.scheduler.afegirEsdeveniment(novaArribada)
            self.entitats_creades += 1
            tempsEntreArribades = 0
        comptador += 1

    def tractarEsdeveniment(self, event):

        if (event.type == EventType.NOVA_ARRIBADA):
            self.ProgramaNovesArribades(event.entitat)

    def afegirCua(self, passatger):
        self.cua.cua.append(passatger)

    def summary(self):
        print('Entitats arribades al sistema: ', self.entitats_creades)

    def GenerateDistribution(self):
        # Definim distribució explicada a la memòria
        if (int((self.config.passatgers)) % 2) == 0:
            X1 = gfg = np.random.triangular(
                2, 10, 16, int(int(self.config.passatgers) / 2))
            X2 = gfg = np.random.triangular(
                12, 17, 22, int(int(self.config.passatgers) / 2))
            X = np.concatenate([X1, X2])
        else:
            # Al ser imparell, posem 1 més a la part inicial del dia
            X1 = gfg = np.random.triangular(
                2, 10, 16, 1 + int(int(self.config.passatgers) / 2))
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
