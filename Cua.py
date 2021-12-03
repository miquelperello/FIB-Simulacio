
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
        return self.mostradors.return_mida_mostradors()
        
        
    def eliminaMostradorLliure(self):
        self.mostradors.elimina_mostrador()

    def afegeixMostradorLliure(self):
        self.mostradors.afegeix_mostrador()    
    
    def eliminaPassatgerCua(self, entitat):
        self.cua.remove(entitat)
        
    #El primer passatger que estava fent cua, ara pot anar al mostrador
    def RecuperaPassatgerCua(self, temps):
        
        _passatger = self.cua.pop(0)
        novaArribada = Event(self.mostradors, temps, EventType.PASSATGER_A_MOSTRADOR, _passatger)
        self.scheduler.afegirEsdeveniment(novaArribada)
        #No fem remove pq hem fet pop
        self.eliminaMostradorLliure()

    def tractarEsdeveniment(self, event):

        if(event.type == EventType.ENTRA_A_CUA):
            if(self.mostradorslliures() > 0 ):
                #Definim estat actiu
                self.state = State.ACTIVE
                # TO-DO Distribució. Ara 10 segons temps a fer la cua (arribar al mostrador)
                event = Event(self.mostradors, event.tid + 10, EventType.PASSATGER_A_MOSTRADOR, event.entitat)
                self.scheduler.afegirEsdeveniment(event)
                #Si encara hi ha gent fent cua...
                if((len(self.cua))!=0):
                    self.eliminaPassatgerCua(event.entitat)
                    self.eliminaMostradorLliure()
        #Si el passatger surt del mostrador, s'afegeix un mostrador lliure i s'afegeix al primer passatger
        elif(event.type == EventType.PASSATGER_SURT_MOSTRADOR):
            self.afegeixMostradorLliure()
            if((len(self.cua))!=0):
                self.RecuperaPassatgerCua(event.tid)
            #Sino, cua buida, canviem estat
            else:  
                self.state = State.INACTIVE
            
            
           
