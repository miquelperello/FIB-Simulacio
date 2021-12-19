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
        for item in range(0, len(self.LlistaMostradorsLliures)):

            if (item != None and self.LlistaMostradorsLliures[item].estat == State.ACTIVE):
                return int(1)
        return int(0)

    def elimina_mostrador(self, event):
        # self.LlistaMostradorsLliures.pop(0)

        for item in range(0, len(self.LlistaMostradorsLliures)):
            if (self.LlistaMostradorsLliures[item].estat == State.ACTIVE):
                #print("does it work?")
                self.LlistaMostradorsLliures[item].estat = State.OCCUPIED
                # print(self.LlistaMostradorsLliures[item].estat)
                return item
                break

        # Miro quin mostrador està ACTIU - lliure
        # for item in range(0, len(self.LlistaMostradorsLliures)):
        #    if (item!=None and self.LlistaMostradorsLliures[item].estat == State.ACTIVE):
        #        mostrador_ocupat = self.LlistaMostradorsLliures[item]
            # Mostrador deixa d'estar disponible
        #       eventMostrador = Event(self, event.tid, EventType.MOSTRADOR_OCUPAT, mostrador_ocupat)
        #        self.scheduler.afegirEsdeveniment(eventMostrador)
        #       break

    def afegeix_mostrador(self, event):

        self.LlistaMostradorsLliures[int(
            event.entitat.mostrador_assignat)].estat = State.ACTIVE

        # Miro quin mostrador està OCUPAT
        # for item in range(0, len(self.LlistaMostradorsLliures)):
        # if (item!=None and self.LlistaMostradorsLliures[item].estat == State.OCCUPIED):
        # mostrador_lliure = self.LlistaMostradorsLliures[item]
        # Mostrador disponible
        # eventMostrador = Event(self, event.tid, EventType.MOSTRADOR_LLIURE, mostrador_lliure)
        # self.scheduler.afegirEsdeveniment(eventMostrador)
        # break

    def tractarEsdeveniment(self, event):
        if (event.type == EventType.MOSTRADOR_INICIALITZAT):
            self.LlistaMostradorsLliures.append(event.entitat)

        # elif (event.type==EventType.MOSTRADOR_LLIURE):
            # for item in range(0, len(self.LlistaMostradorsLliures)):
            # if  self.LlistaMostradorsLliures[item] == event.entitat:
            #self.LlistaMostradorsLliures[item].estat = State.ACTIVE
            # break

        # elif(event.type==EventType.MOSTRADOR_OCUPAT):
            # self.LlistaMostradorsLliures.remove(event.entitat)
            # Posem estat a ocupat
            #self.LlistaMostradorsLliures[event.entitat].estat = State.OCCUPIED
            # for item in range(0, len(self.LlistaMostradorsLliures)):
            # if (self.LlistaMostradorsLliures[item] == event.entitat):
            #print("does it work?")
            #self.LlistaMostradorsLliures[item].estat = State.OCCUPIED
            # print(self.LlistaMostradorsLliures[item].estat)
            # break

        elif (event.type == EventType.PASSATGER_A_MOSTRADOR):

            # print(self.LlistaMostradorsLliures[0].estat)

            event.entitat.estat = State.PROCESSING
            event.entitat.temps_entrada_mostrador = event.tid

            # Estadístics
            temps_passatger_CUA = event.entitat.temps_entrada_mostrador - \
                event.entitat.temps_entrada_cua
            # Si es 0, no hay que hacer calculo
            if(self.scheduler.temps_mitja_CUA != 0):
                self.scheduler.temps_mitja_CUA = (
                    self.scheduler.temps_mitja_CUA + temps_passatger_CUA)/2
            else:
                self.scheduler.temps_mitja_CUA = temps_passatger_CUA

            tempsFacturacio = np.random.triangular(120, 240, 900)
            for i in range(0, event.entitat.maleta):
                # TO-DO Posar distribució
                tempsFacturacio += np.random.triangular(60, 60, 300)

            # Creem l'esdeveniment passatger
            eventPassatger = Event(self.cua, event.tid + tempsFacturacio,
                                   EventType.PASSATGER_SURT_MOSTRADOR, event.entitat)
            self.scheduler.afegirEsdeveniment(eventPassatger)

        elif (event.type == EventType.PASSATGER_SURT_MOSTRADOR):
            self.LlistaMostradorsLliures.append(1)

        elif(event.type == EventType.CANVI_DE_TORN):
            if(event.tid == 28800):
                self.config.mostradors = 6
            elif(event.tid == 57600):
                self.config.mostradors = 4
            elif(event.tid == 73800):
                self.config.mostradors = 6
