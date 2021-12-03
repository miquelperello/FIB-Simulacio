import bisect
from Event import *
from Source import *
 
from Config import *
import time

class Scheduler:

    currentTime = 0
    eventList = []
    simulationStart =""

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
        while self.currentTime<1000:
            #recuperem event simulacio
             if ((len(self.eventList) != 0)):
                 event=Scheduler.eventList.pop(0)
                 attrs = vars(event)
                 print("Esdeveniment a tractar " + ', '.join("%s: %s" % item for item in attrs.items()))
                 # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat            
                 event.objekt.tractarEsdeveniment(event)
                 
            
            #actualitzem el rellotge de simulacio
             self.currentTime=event.tid
                     
        #recollida d'estadístics
        # self.recollirEstadistics()





    def inicialitzaesdeveniments(self):
        self.mostradors.inicialitzaMostradors()
        self.source.SimulationStart()
        

    
    def afegirEsdeveniment(self, event):
        #inserir esdeveniment de forma ordenada
        bisect.insort(self.eventList, event)
        a=10

        
    def crearModel(self):
        self.Config =  Config()
        self.mostradors = Mostradors(self, self.Config)
        self.Cua = Cua(self, self.mostradors)
        self.source = Source(self, self.Config, self.Cua)
        #TO-DO Refactor
        self.mostradors.connecta(self.Cua)       
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

             

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
