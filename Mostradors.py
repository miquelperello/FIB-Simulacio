from auxiliar import *
from Config import *
from Event import *
import numpy as np
import matplotlib.pyplot as plt


class Mostradors:

    LlistaMostradorsLliures = []

    def __init__(self):
        self.estat = State.ACTIVE

    def inicialitzaMostradors(self):
        for i in range(0, int(self.config.mostradors)):
            self.LlistaMostradorsLliures.append(i)

    def connecta(self, cua, config, scheduler):
        self.cua = cua
        self.scheduler = scheduler
        self.config = config

    def return_mostradors_lliures(self):
        # Mirem pels Mostradors actuals disponibles, si hi ha algun amb estat ACTIVE
        for item in range(0, int(self.config.mostradors)):
            if (item != None and self.LlistaMostradorsLliures[item].estat == State.ACTIVE):
                return 1
        return 0

    def elimina_mostrador(self, event):
        # Mirem pels Mostradors actuals disponibles, si hi ha algun amb estat ACTIVE, el deixem com a OCUPAT i el retornem

        for item in range(0, int(self.config.mostradors)):
            if (self.LlistaMostradorsLliures[item].estat == State.ACTIVE):
                self.LlistaMostradorsLliures[item].estat = State.OCCUPIED
                return item
                break

    def afegeix_mostrador(self, event):
        # Per l'event passat per paràmetre, on obtenim el passatger i el seu mostrador assignat, el deixem en ACTIVE.
        self.LlistaMostradorsLliures[int(
            event.entitat.mostrador_assignat)].estat = State.ACTIVE

    def tractarEsdeveniment(self, event):
        if (event.type == EventType.MOSTRADOR_INICIALITZAT):
            self.LlistaMostradorsLliures.append(event.entitat)

        elif (event.type == EventType.PASSATGER_A_MOSTRADOR):

            event.entitat.estat = State.PROCESSING
            event.entitat.temps_entrada_mostrador = event.tid

            # Estadístics
            temps_passatger_CUA = event.entitat.temps_entrada_mostrador - \
                event.entitat.temps_entrada_cua
            # Si es 0, no cal fer càlcul.
            if(self.scheduler.temps_mitja_CUA != 0):
                self.scheduler.temps_mitja_CUA = (
                    self.scheduler.temps_mitja_CUA + temps_passatger_CUA)/2
            else:
                self.scheduler.temps_mitja_CUA = temps_passatger_CUA

            # Càlcul de temps de facturació
            tempsFacturacio = np.random.triangular(120, 240, 900)
            for i in range(0, event.entitat.maleta):
                tempsFacturacio += np.random.triangular(60, 60, 300)

            # Creem l'esdeveniment passatger
            eventPassatger = Event(self.cua, event.tid + tempsFacturacio,
                                   EventType.PASSATGER_SURT_MOSTRADOR, event.entitat)
            self.scheduler.afegirEsdeveniment(eventPassatger)

        elif(event.type == EventType.CANVI_DE_TORN):
            # Definim els mostradors disponibles segons el torn
            if(event.tid == 28800):
                self.config.mostradors = self.config.mostradors2
            elif(event.tid == 57600):
                self.config.mostradors = self.config.mostradors3
            elif(event.tid == 73800):
                self.config.mostradors = 0
                self.estat = State.INACTIVE
