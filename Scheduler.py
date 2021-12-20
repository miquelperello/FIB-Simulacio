import bisect
from Event import *
from Source import *
from Config import *


class Scheduler:

    currentTime = 0
    eventList = []
    simulationStart = ""
    pa_cua = 0
    pa_mostra = 0
    pa_surt_mostra = 0
    temps_mitja_CUA = 0
    temps_mitja_CUA_SORTIDA = 0
    temps_mitja_MOSTRADOR = 0
    pa_han_perdut_avio = 0

    def __init__(self):
        # creació dels objectes que composen el meu model
        self.simulationStart = Event(self, 0, EventType.SimulationStart, None)
        self.afegirEsdeveniment(self.simulationStart)

    def run(self):
        # configurar el model per consola
        self.crearModel()
        self.Config.configurarModel()

        # rellotge de simulacio a 0
        self.currentTime = 0
        # bucle de simulació (condició fi simulació: fi jornada)
        while self.currentTime < 78000:
            # recuperem event simulacio
            if ((len(self.eventList) != 0)):
                event = Scheduler.eventList.pop(0)
                self.trace(event)
                # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
                event.objekt.tractarEsdeveniment(event)

            # actualitzem el rellotge de simulacio
            self.currentTime = event.tid
        # recollida d'estadistics
        self.recollirEstadistics()

    def trace(self, event):

        color = Colors.HEADER
        if event.type == EventType.ENTRA_A_CUA:
            color = Colors.OKBLUE
            self.pa_cua += 1
        elif event.type == EventType.PASSATGER_A_MOSTRADOR:
            color = Colors.HEADER
            self.pa_mostra += 1
        elif event.type == EventType.PASSATGER_SURT_MOSTRADOR:
            color = Colors.OKGREEN
            self.pa_surt_mostra += 1
        elif event.type == EventType.MOSTRADOR_INICIALITZAT:
            color = Colors.OKCYAN
        elif event.type == EventType.SimulationStart:
            color = Colors.OKRARO
        elif event.type == EventType.CANVI_DE_TORN:
            color = Colors.WARNING
        elif event.type == EventType.SimulationEnd:
            color = Colors.FAIL

        if (self.Config.veuretraza == 0):
            return
        elif (self.Config.veuretraza == 1):
            print(color, event.tid, event.type, ' ', event.objekt, Colors.ENDC)

    def inicialitzaesdeveniments(self):
        self.source.SimulationStart()

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        bisect.insort(self.eventList, event)
        a = 10

    def crearModel(self):
        self.Config = Config()
        self.mostradors = Mostradors()
        self.Cua = Cua(self, self.mostradors)
        self.source = Source(self, self.Config, self.Cua, self.mostradors)
        self.mostradors.connecta(self.Cua, self.Config, self)

    def returnLlistaEsdeveniments(self):
        global eventList
        return Scheduler.eventList

    def tractarEsdeveniment(self, event):

        if (event.type == EventType.SimulationStart):
            # comunicar a tots els objectes que cal preparar-se
            self.inicialitzaesdeveniments()

    def summary(self):

        print('Entitats entrades a la cua: ', self.pa_cua)
        print('Entitats que han entrat al mostrador: ', self.pa_mostra)
        print('Entitats que han sortit del mostrador: ', self.pa_surt_mostra)

        print('Temps mitjà a la cua: ', round(self.temps_mitja_CUA, 2),
              "s. ", round(self.temps_mitja_CUA/60, 2), "min.", round(self.temps_mitja_CUA/3600, 2), "h.")
        print('Temps mitjà al mostrador: ', round(self.temps_mitja_MOSTRADOR, 2),
              "s. ", round(self.temps_mitja_MOSTRADOR/60, 2), "min.", round(self.temps_mitja_MOSTRADOR/3600, 2), "h.")
        print('Temps mitjà total: ', round(self.temps_mitja_CUA_SORTIDA, 2),
              "s. ", round(self.temps_mitja_CUA_SORTIDA/60, 2), "min.", round(self.temps_mitja_CUA_SORTIDA/3600, 2), "h.")

        print('Passatgers que han perdut l\'avió: ', self.pa_han_perdut_avio)

    def recollirEstadistics(self):
        print(Colors.HEADER, "ESTADÍSTICS", Colors.ENDC)

        self.source.summary()
        self.summary()


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
