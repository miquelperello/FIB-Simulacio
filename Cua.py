
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
        
    #El primer passatger que estava fent cua, ara pot anar al mostrador
    def RecuperaPassatgerCua(self, event):
        
        _passatger = self.cua[0]
        #_passatger.estat = State.WAITING
        #_passatger.temps_entrada_cua =  event.tid + 10
        novaArribada = Event(self.mostradors, event.tid+_passatger.temps, EventType.PASSATGER_A_MOSTRADOR, _passatger)
        self.scheduler.afegirEsdeveniment(novaArribada)
        #Eliminem passatger de la cua
        
        #print(_passatger.temps_entrada_cua)
        if(event.tid > _passatger.temps_entrada_cua):
            self.cua.pop(0)
       
        

    def tractarEsdeveniment(self, event):

        if(event.type == EventType.ENTRA_A_CUA):
            if(self.mostradorslliures() > 0 ):
                #Definim estat actiu
                event.entitat.estat = State.WAITING
                event.entitat.temps_entrada_cua = event.tid
                # TO-DO Distribució. Ara 10 segons temps a fer la cua (arribar al mostrador)
                event = Event(self.mostradors, event.tid + 10, EventType.PASSATGER_A_MOSTRADOR, event.entitat)
                #Posem al passatger el temps de mostrador
                event.entitat.temps = event.tid + 10
                self.scheduler.afegirEsdeveniment(event)
                #Si encara hi ha gent fent cua...
                
                if((len(self.cua))!=0):
                    self.eliminaPassatgerCua(event.entitat)
                    mostrador_lliure = self.eliminaMostradorLliure(event)
                    #Assignem Mostrador a Passatger
                    event.entitat.mostrador_assignat = mostrador_lliure


        #Si el passatger surt del mostrador, s'afegeix un mostrador lliure i s'afegeix al primer passatger
        elif(event.type == EventType.PASSATGER_SURT_MOSTRADOR):
            self.afegeixMostradorLliure(event)
            
            if((len(self.cua))!=0):
                event.entitat.temps_sortida_mostrador = event.tid
                temps_passatger_CUA_SORTIDA = event.entitat.temps_sortida_mostrador - event.entitat.temps_entrada_cua
                self.scheduler.temps_mitja_CUA_SORTIDA = (self.scheduler.temps_mitja_CUA_SORTIDA + temps_passatger_CUA_SORTIDA)/2
                
                temps_passatger_MOSTRADOR = event.entitat.temps_sortida_mostrador - event.entitat.temps_entrada_mostrador
                self.scheduler.temps_mitja_MOSTRADOR = (self.scheduler.temps_mitja_MOSTRADOR + temps_passatger_MOSTRADOR)/2
                
                #TO-DO Enviem a gent que encara no està a la cua
                mostrador_lliure = self.eliminaMostradorLliure(event)
                event.entitat.mostrador_assignat = mostrador_lliure
                self.RecuperaPassatgerCua(event)
                #print("###Resultats passatger: ", event.entitat.temps_entrada_cua, " ", event.entitat.temps_entrada_mostrador, " ", event.entitat.temps_sortida_mostrador)
    
            #Sino, cua buida, canviem estat
            else:  
                self.state = State.INACTIVE
                event.entitat.temps_sortida_mostrador = event.tid
                #print("###Resultats passatger: ", event.entitat.temps_entrada_cua, " ", event.entitat.temps_entrada_mostrador, " ", event.entitat.temps_sortida_mostrador)
            
            
           
