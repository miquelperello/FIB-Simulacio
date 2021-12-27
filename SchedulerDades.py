import bisect
import os
from Event import *
from Source import *
from ConfigDades import *
import csv
import os.path


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
    parser = ""

    def __init__(self):
        # creació del primer event per crear Objectes
        self.simulationStart = Event(self, 0, EventType.SimulationStart, None)
        self.afegirEsdeveniment(self.simulationStart)

    def run(self):
        # configurar el model per consola
        self.crearModel()
        self.config.configurarModel()

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
        # self.recollirEstadistics()

    def trace(self, event):
        if (self.config.veuretraza == 'No'):
            return
        elif (self.config.veuretraza == 'Si'):
            color = Colors.HEADER
            if event.type == EventType.ENTRA_A_CUA:
                color = Colors.OKBLUE
            elif event.type == EventType.PASSATGER_A_MOSTRADOR:
                color = Colors.HEADER
            elif event.type == EventType.PASSATGER_SURT_MOSTRADOR:
                color = Colors.OKGREEN
            elif event.type == EventType.MOSTRADOR_INICIALITZAT:
                color = Colors.OKCYAN
            elif event.type == EventType.CANVI_DE_TORN:
                color = Colors.WARNING
            elif event.type == EventType.SimulationEnd:
                color = Colors.FAIL

            print(color, event.tid, event.type, ' ', event.objekt, Colors.ENDC)

    def inicialitzaesdeveniments(self):
        self.source.SimulationStart()

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        bisect.insort(self.eventList, event)
        a = 10

    def crearModel(self):
        # Creem instàncies i connectem referències
        self.config = ConfigDades()
        self.mostradors = Mostradors()
        self.cua = Cua()
        self.source = Source()

        self.cua.connecta(self, self.mostradors)
        self.source.connecta(self, self.config, self.cua, self.mostradors)
        self.mostradors.connecta(self.cua, self.config, self)

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

        if (self.config.csv == 'Si'):
            dades_csv = []
            dades_csv.append(int(self.config.mostradors1))
            dades_csv.append(int(self.config.mostradors2))
            dades_csv.append(int(self.config.mostradors3))
            dades_csv.append(int(self.config.passatgers))
            dades_csv.append(int(round(self.temps_mitja_CUA, 2)))
            dades_csv.append(int(round(self.temps_mitja_MOSTRADOR, 2)))
            dades_csv.append(int(round(self.temps_mitja_CUA_SORTIDA, 2)))
            dades_csv.append(int(self.pa_han_perdut_avio))

            headerList = [
                'Temps a la cua', "Temps al mostrador",
                "Temps entrada a cua fins sortida mostrador",
                "Persones que han perdut l'avió"]

            filename = 'export.csv'
            file_exists = os.path.isfile(filename)

            with open(filename, 'a') as csvfile:
                headers = ['1rTorn', '2nTorn',
                           '3rTorn', 'Passatgers', 'TempsCua', 'TempsMostrador',
                           'TempsCuaSortida', 'PerdAvio']
                writer = csv.DictWriter(
                    csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)

                if not file_exists:
                    writer.writeheader()  # file doesn't exist yet, write a header

                writer.writerow(
                    {'1rTorn': dades_csv[0], '2nTorn': dades_csv[1], '3rTorn': dades_csv[2], 'Passatgers': dades_csv[3], 'TempsCua': dades_csv[4], 'TempsMostrador': dades_csv[5], 'TempsCuaSortida': dades_csv[6], 'PerdAvio': dades_csv[7]})

    def recollirEstadistics(self):
        print(Colors.HEADER, "ESTADÍSTICS", Colors.ENDC)

        self.source.summary()
        self.summary()


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
