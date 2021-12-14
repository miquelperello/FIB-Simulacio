import bisect
from Event import *
from Source import *

from Config import *

import time

class Scheduler:

    currentTime = 0
    eventList = []
    simulationStart =""
    pa_cua = 0
    pa_mostra = 0
    pa_surt_mostra = 0
    temps_mitja_CUA_SORTIDA = 0
    temps_mitja_MOSTRADOR = 0

    def __init__(self):
        # creació dels objectes que composen el meu model
        self.simulationStart=Event(self,0,EventType.SimulationStart,None)
        self.afegirEsdeveniment(self.simulationStart)
 
         
        
        
        
        

    

    def run(self):
        #configurar el model per consola, arxiu de text...
        self.crearModel()
        self.Config.configurarModel()

        #rellotge de simulacio a 0
        self.currentTime=0        
        #bucle de simulació (condició fi simulació llista buida)
        while self.currentTime<70000:
            #recuperem event simulacio
             if ((len(self.eventList) != 0)):
                 event=Scheduler.eventList.pop(0)
                 self.trace(event)
                 # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat            
                 event.objekt.tractarEsdeveniment(event)
                 
            
            #actualitzem el rellotge de simulacio
             self.currentTime=event.tid
        #recollida d'estadistics
        self.recollirEstadistics()             
        # self.recollirEstadistics()


    def trace(self,event):
            if (self.Config.veuretraza==0):
                return
            elif (self.Config.veuretraza ==1):
                color=Colors.HEADER
                if event.type==EventType.ENTRA_A_CUA:
                    color=Colors.OKBLUE
                    self.pa_cua +=1
                elif event.type==EventType.PASSATGER_A_MOSTRADOR:
                    color=Colors.HEADER
                    self.pa_mostra +=1
                elif event.type==EventType.PASSATGER_SURT_MOSTRADOR:
                    color=Colors.OKGREEN
                    self.pa_surt_mostra +=1
                elif event.type==EventType.MOSTRADOR_INICIALITZAT:
                    color=Colors.OKCYAN
                elif event.type==EventType.SimulationStart:
                    color=Colors.OKRARO
                elif event.type==EventType.CANVI_DE_TORN:
                    color=Colors.OKRANDOM
                
                print(color,event.tid,event.type,' ',event.objekt,Colors.ENDC)


    def inicialitzaesdeveniments(self):
        self.source.SimulationStart()
        

    
    def afegirEsdeveniment(self, event):
        #inserir esdeveniment de forma ordenada
        bisect.insort(self.eventList, event)
        a=10

        
    def crearModel(self):
        self.Config =  Config()
        self.mostradors = Mostradors()
        self.Cua = Cua(self, self.mostradors)
        self.source = Source(self, self.Config, self.Cua, self.mostradors)
        #TO-DO Refactor
        self.mostradors.connecta(self.Cua, self.Config, self)       
        #self.mostradors.inicialitzaMostradors(self.Config)  



    def returnLlistaEsdeveniments(self):
        global eventList
        return Scheduler.eventList

    def tractarEsdeveniment(self,event):
        
        if (event.type==EventType.SimulationStart):
            # comunicar a tots els objectes que cal preparar-se            
            self.inicialitzaesdeveniments()

        elif (event.type=="ENTRA_A_CUA"):
            self.Cua.AfegirPassatgersCua(event.temps, self.eventList)



    def summary(self):
        
        
        print('Entitats entrades a la cua: ',self.pa_cua) 
        print('Entitats que han entrat al mostrador: ',self.pa_mostra)
        print('Entitats que han sortit del mostrador: ',self.pa_surt_mostra)
        print('Temps mitjà fent total: ',self.temps_mitja_CUA_SORTIDA)
        print('Temps mitjà al mostrador: ',self.temps_mitja_MOSTRADOR)

    def recollirEstadistics(self):
        print(Colors.HEADER,"ESTADÍSTICS",Colors.ENDC)

        self.source.summary()
        self.summary()   

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
