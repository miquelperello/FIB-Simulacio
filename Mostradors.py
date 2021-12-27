from auxiliar import *
from Config import *
from Event import *
import numpy as np
import matplotlib.pyplot as plt


class Mostradors:

    LlistaMostradorsLliures = []

    def __init__(self):
        self.estat = State.ACTIVE

    def connecta(self, cua, config, scheduler):
        # Connectem classes
        self.cua = cua
        self.scheduler = scheduler
        self.config = config

    def return_mostrador_lliures(self):
        # Mirem pels Mostradors actuals disponibles, si hi ha algun amb estat ACTIVE
        for item in range(0, int(self.config.mostradors)):
            if (item != None and self.LlistaMostradorsLliures[item].estat == State.ACTIVE):
                return 1
        return 0

    def elimina_mostrador_lliure(self):
        # Mirem pels Mostradors actuals disponibles, si hi ha algun amb estat ACTIVE, el deixem com a OCUPAT i el retornem
        for item in range(0, int(self.config.mostradors)):
            if (self.LlistaMostradorsLliures[item].estat == State.ACTIVE):
                self.LlistaMostradorsLliures[item].estat = State.OCCUPIED
                return item
                break

    def afegeix_mostrador_lliure(self, event):
        # Per l'event passat per paràmetre, on obtenim el passatger i el seu mostrador assignat, el deixem en ACTIVE.
        self.LlistaMostradorsLliures[int(
            event.entitat.mostrador_assignat)].estat = State.ACTIVE

    def defineixTempsCua(self):
        # Pels passatgers que segueixen a la cua, com s'ha tancat el procés de check in, els deixem el seu temps de
        # cua final com el temps actual.
        for i in self.cua.cua:
            temps_passatger_CUA = (73800 - i.temps_entrada_cua)
            if(self.scheduler.temps_mitja_CUA != 0):
                self.scheduler.temps_mitja_CUA = (
                    self.scheduler.temps_mitja_CUA + temps_passatger_CUA)/2
            else:
                self.scheduler.temps_mitja_CUA = temps_passatger_CUA

    def tractarEsdeveniment(self, event):
        if (event.type == EventType.MOSTRADOR_INICIALITZAT):
            self.LlistaMostradorsLliures.append(event.entitat)

        elif (event.type == EventType.PASSATGER_A_MOSTRADOR):
            # Definim estat
            event.entitat.estat = State.PROCESSING
            # Actualitzem temps d'entrada al mostrador
            event.entitat.temps_entrada_mostrador = event.tid

            # Estadístics

            # Actualitzem passatgers a mostrador estadístic
            self.scheduler.pa_mostra += 1

            # Actualitzem temps
            temps_passatger_CUA = event.entitat.temps_entrada_mostrador - \
                event.entitat.temps_entrada_cua
            # Si és 0, no cal fer càlcul.
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
            eventPassatger = Event(self.cua, event.tid + int(tempsFacturacio),
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
                self.defineixTempsCua()
            # Si s'acaba d'incorporar algun treballador i tenim mostrador lliure...
            if((len(self.cua.cua)) > 0 and self.return_mostrador_lliures()):
                # Seleccionem el mostrador lliure, que l'acaba de deixar el passatger de l'event.
                mostrador_lliure = self.cua.eliminaMostradorLliure()
                # Recuperem al passatger de la cua
                self.cua.RecuperaPassatgerCua(event, mostrador_lliure)
