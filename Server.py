#millor treballar amb define o algun sistema simular a l'enum de C++
from Server import *
from Event import *

class Server:

    def __init__(self,scheduler):
        # inicialitzar element de simulació
        entitatsTractades=0
        self.state=idle
        self.scheduler=scheduler
        self.entitatActiva=null
        
    def crearConnexio(self,server2,queue):
        self.queue=queue
        self.server=server2
    
    def recullEntitat(self,time,entitat):
        self.entitatsTractades=entitat
        self.programarFinalServei(time,entitat)

    def tractarEsdeveniment(self, event):
        if (event.tipus=='SIMULATION START'):
            self.simulationStart(event)

        if (event.tipus=='END_SERVICE'):
            self.processarFiServei(event)

    def simulationStart(self,event):
        self.state=idle
        self.entitatsTractades=0

    def programarFinalServei(self, time,entitat):
        # que triguem a fer un servei (aleatorietat)
        tempsServei = _alguna_funcio ()
        # incrementem estadistics si s'escau
        self.entitatsTractades=self.entitatsTractades+1
        self.state = busy
        # programació final servei
        return Event(self,'END_SERVICE', time+ tempsServei,entitat)

    def processarFiServei(self,event):
        # Registrar estadístics
        self.entitatsTractades=self.entitatsTractades+1
        # Mirar si es pot transferir a on per toqui
        if (server.estat==idle):
            #transferir entitat (es pot fer amb un esdeveniment immediat o invocant a un métode de l'element)
            server.recullEntitat(event.time,event.entitat)
        else:
            if (queue.estat==idle):
                queue.recullEntitat(event.time,event.entitat)
            ...
        self.estat=idle
    
    ... 

        
