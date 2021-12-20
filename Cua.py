
from Passatger import *
from Mostradors import *
from Event import *
from auxiliar import *


class Cua:

    cua = []

    def __init__(self, scheduler, mostradors):
        cua = []
        self.mostradors = mostradors
        self.scheduler = scheduler
        self.state = State.INACTIVE

    def AfegirPassatgersCua(self, temps, eventLlista):
        passatger = Passatger(temps)
        self.cua.append(passatger)
        self.gestionaPassatgers(temps, eventLlista)

    def mostradorslliures(self):
        return self.mostradors.return_mostradors_lliures()

    def eliminaMostradorLliure(self, event):
        return self.mostradors.elimina_mostrador(event)

    def afegeixMostradorLliure(self, event):
        self.mostradors.afegeix_mostrador(event)

    def eliminaPassatgerCua(self, entitat):
        self.cua.remove(entitat)

    # El primer passatger que estava fent cua, ara pot anar al mostrador
    def RecuperaPassatgerCua(self, event):

        _passatger = self.cua[0]
        #_passatger.estat = State.WAITING
        #_passatger.temps_entrada_cua =  event.tid + 10
        novaArribada = Event(self.mostradors, event.tid+_passatger.temps,
                             EventType.PASSATGER_A_MOSTRADOR, _passatger)
        self.scheduler.afegirEsdeveniment(novaArribada)
        # Eliminem passatger de la cua

        # print(_passatger.temps_entrada_cua)
        self.cua.pop(0)

    def tractarEsdeveniment(self, event):

        if(event.type == EventType.ENTRA_A_CUA):
            # Primer, afegeixo el passatger a la cua
            self.cua.append(event.entitat)
            # Poso a estat WAITING
            event.entitat.estat = State.WAITING
            # Li assigno el temps
            event.entitat.temps_entrada_cua = event.tid
            # Si no hi ha ningú fent cua

            # Si hi ha algun mostrador lliure
            if(self.mostradorslliures() > 0):

                event = Event(self.mostradors, event.tid,
                              EventType.PASSATGER_A_MOSTRADOR, event.entitat)
                # Posem al passatger el temps de mostrador
                event.entitat.temps = event.tid
                # L'eliminem de la cua
                self.eliminaPassatgerCua(event.entitat)
                # Li assignem un mostrador
                mostrador_lliure = self.eliminaMostradorLliure(event)
                # Assignem Mostrador a Passatger
                event.entitat.mostrador_assignat = mostrador_lliure
                # Afegim event
                self.scheduler.afegirEsdeveniment(event)

        # Si el passatger surt del mostrador, s'afegeix un mostrador lliure i s'afegeix al primer passatger
        elif(event.type == EventType.PASSATGER_SURT_MOSTRADOR):
            self.afegeixMostradorLliure(event)

            # Estadístics
            event.entitat.temps_sortida_mostrador = event.tid
            temps_passatger_CUA_SORTIDA = event.entitat.temps_sortida_mostrador - \
                event.entitat.temps_entrada_cua
            # Si es 0, no hay que hacer calculo
            if(self.scheduler.temps_mitja_CUA_SORTIDA != 0):
                self.scheduler.temps_mitja_CUA_SORTIDA = (
                    self.scheduler.temps_mitja_CUA_SORTIDA + temps_passatger_CUA_SORTIDA)/2
            else:
                self.scheduler.temps_mitja_CUA_SORTIDA = temps_passatger_CUA_SORTIDA

            temps_passatger_MOSTRADOR = event.entitat.temps_sortida_mostrador - \
                event.entitat.temps_entrada_mostrador
            if(self.scheduler.temps_mitja_MOSTRADOR != 0):
                self.scheduler.temps_mitja_MOSTRADOR = (
                    self.scheduler.temps_mitja_MOSTRADOR + temps_passatger_MOSTRADOR)/2
            else:
                self.scheduler.temps_mitja_MOSTRADOR = temps_passatger_MOSTRADOR

            if (temps_passatger_CUA_SORTIDA > 7200):
                event.entitat.perd_avio = 1
                self.scheduler.pa_han_perdut_avio += 1

            if((len(self.cua)) != 0):

                mostrador_lliure = self.eliminaMostradorLliure(event)
                event.entitat.mostrador_assignat = mostrador_lliure
                self.RecuperaPassatgerCua(event)
                # print("###Resultats passatger: ", event.entitat.temps_entrada_cua, " ", event.entitat.temps_entrada_mostrador, " ", event.entitat.temps_sortida_mostrador)

            # Sino, cua buida, canviem estat
            else:
                self.state = State.INACTIVE
                # print("###Resultats passatger: ", event.entitat.temps_entrada_cua, " ", event.entitat.temps_entrada_mostrador, " ", event.entitat.temps_sortida_mostrador)
