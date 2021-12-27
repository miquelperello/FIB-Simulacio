from tkinter.constants import S
from Passatger import *
from Mostradors import *
from Event import *
from auxiliar import *


class Cua:

    cua = []

    def __init__(self):
        self.state = State.ACTIVE

    def connecta(self, scheduler, mostradors):
        # Connectem referències amb les altres classes
        self.mostradors = mostradors
        self.scheduler = scheduler

    def mostradorslliures(self):
        return self.mostradors.return_mostrador_lliures()

    def eliminaMostradorLliure(self):
        return self.mostradors.elimina_mostrador_lliure()

    def afegeixMostradorLliure(self, event):
        self.mostradors.afegeix_mostrador_lliure(event)

    def eliminaPassatgerCua(self, entitat):
        self.cua.remove(entitat)

    # El primer passatger que estava fent cua, ara pot anar al mostrador
    def RecuperaPassatgerCua(self, event, mostrador_lliure):
        """"
        Agafa al primer passatger a la cua, i l'envia al mostrador
        :event: l'event de Sortida del Mostrador.
        :mostrador_lliure: el mostrador lliure per assignar
        """
        # Seleccionem el primer passatger de la cua
        _passatger = self.cua.pop(0)
        # Li assignem el mostrador lliure
        _passatger.mostrador_assignat = mostrador_lliure
        # Creem Event amb temps sortida cua anterior + temps cua passatger
        novaArribada = Event(self.mostradors, event.tid+_passatger.temps,
                             EventType.PASSATGER_A_MOSTRADOR, _passatger)
        self.scheduler.afegirEsdeveniment(novaArribada)

    def tractarEsdeveniment(self, event):

        if(event.type == EventType.ENTRA_A_CUA):
            # Augmentem usuaris a cua -> Estadístic scheduler
            self.scheduler.pa_cua += 1
            # Primer, afegeixo el passatger a la cua
            self.cua.append(event.entitat)
            # Poso passatger a estat WAITING
            event.entitat.estat = State.WAITING
            # Li assigno el temps
            event.entitat.temps_entrada_cua = event.tid
            # Si hi ha algun mostrador lliure
            if(self.mostradorslliures() > 0):
                # Creem event per anar al mostrador
                event = Event(self.mostradors, event.tid,
                              EventType.PASSATGER_A_MOSTRADOR, event.entitat)
                # Posem al passatger el temps de mostrador
                event.entitat.temps = event.tid
                # L'eliminem de la cua
                self.eliminaPassatgerCua(event.entitat)
                # Li assignem un mostrador
                mostrador_lliure = self.eliminaMostradorLliure()
                # Assignem Mostrador a Passatger
                event.entitat.mostrador_assignat = mostrador_lliure
                # Afegim event
                self.scheduler.afegirEsdeveniment(event)

        # Si el passatger surt del mostrador, s'afegeix un mostrador lliure i s'afegeix al primer passatger
        elif(event.type == EventType.PASSATGER_SURT_MOSTRADOR):
            # Definim estat a inactiu
            event.entitat.estat = State.INACTIVE

            # Definim el mostrador tractat com a lliure
            self.afegeixMostradorLliure(event)

            # Estadístics

            # Actualitzem passatgers surten de mostrador - estadístic
            self.scheduler.pa_surt_mostra += 1
            # Temps Cua Sortida
            event.entitat.temps_sortida_mostrador = event.tid
            temps_passatger_CUA_SORTIDA = event.entitat.temps_sortida_mostrador - \
                event.entitat.temps_entrada_cua
            # Si es 0, no s'ha de fer la mitja.
            if(self.scheduler.temps_mitja_CUA_SORTIDA != 0):
                self.scheduler.temps_mitja_CUA_SORTIDA = (
                    self.scheduler.temps_mitja_CUA_SORTIDA + temps_passatger_CUA_SORTIDA)/2
            else:
                self.scheduler.temps_mitja_CUA_SORTIDA = temps_passatger_CUA_SORTIDA

            # Temps Mostrador
            temps_passatger_MOSTRADOR = event.entitat.temps_sortida_mostrador - \
                event.entitat.temps_entrada_mostrador
            if(self.scheduler.temps_mitja_MOSTRADOR != 0):
                self.scheduler.temps_mitja_MOSTRADOR = (
                    self.scheduler.temps_mitja_MOSTRADOR + temps_passatger_MOSTRADOR)/2
            else:
                self.scheduler.temps_mitja_MOSTRADOR = temps_passatger_MOSTRADOR

            # Si el passatger fa 2h desde l'entrada a la cua, ha perdut l'avió
            if (temps_passatger_CUA_SORTIDA > 7200):
                event.entitat.perd_avio = 1
                self.scheduler.pa_han_perdut_avio += 1
            # Si encara queden passatgers a la cua, enviem al primer de la cua a un mostrador lliure
            # Definim el mostradorslliures() ja que, tot i acabar d'alliberar un mostrador, és possible que sigui fora d'horari (últim torn) i no hi hagi cap.
            if((len(self.cua)) > 0 and self.mostradorslliures()):
                # Seleccionem el mostrador lliure, que l'acaba de deixar el passatger de l'event.
                mostrador_lliure = self.eliminaMostradorLliure()
                # Recuperem al passatger de la cua
                self.RecuperaPassatgerCua(event, mostrador_lliure)

            # Sino, cua buida, canviem estat
            else:
                self.state = State.INACTIVE
