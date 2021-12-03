from auxiliar import * 
from Config import * 
from Event import *

class Mostradors:
    
    
    LlistaMostradorsLliures = []
    
    def __init__(self, scheduler, config):
        self.estat = "0"
        self.scheduler = scheduler
        self.config = config
        
    def inicialitzaMostradors(self):
        for i in range (0, int(self.config.mostradors)):
            self.LlistaMostradorsLliures.append(i)
        
    def connecta(self, cua):
        self.cua = cua    

    def return_mida_mostradors(self):
        return len(self.LlistaMostradorsLliures)

    
    def elimina_mostrador(self):
        self.LlistaMostradorsLliures.pop(0)

    def afegeix_mostrador(self):
        self.LlistaMostradorsLliures.append(1)    

        

    def tractarEsdeveniment(self, event):
        if (event.type==EventType.PASSATGER_A_MOSTRADOR):
            
            tempsFacturacio = 0
            for i in range(0, event.entitat.maleta):
                #TO-DO Posar distribució
                tempsFacturacio+= 5

            event = Event(self.cua, event.tid + tempsFacturacio, EventType.PASSATGER_SURT_MOSTRADOR, event.entitat)
            self.scheduler.afegirEsdeveniment(event)
        elif (event.type==EventType.PASSATGER_SURT_MOSTRADOR):
            self.LlistaMostradorsLliures.append(1)      