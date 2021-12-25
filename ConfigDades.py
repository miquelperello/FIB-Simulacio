import Scheduler
from Mostradors import *
from datetime import *
import argparse


class ConfigDades:
    mostradors = "None"
    mostradors1 = "None"
    mostradors2 = "None"
    mostradors3 = "None"

    treballadors = "None"
    passatgers = "None"
    veuretraza = "None"
    csv = "None"
    iteracions = "None"
    parser = "None"

    def __init__(self):
        global parser
        self.state = "inactiu"
        parser = argparse.ArgumentParser()
        parser.add_argument("-m1",
                            "--mostrador1",
                            help="Defineix el num de mostradors disponibles al primer torn, de 02:00h a 12:00h",
                            type=int)

        parser.add_argument("-m2",
                            "--mostrador2",
                            help="Defineix el num de mostradors disponibles al segon torn, de 12:00h a 18:00h",
                            type=int)

        parser.add_argument("-m3",
                            "--mostrador3",
                            help="Defineix el num de mostradors disponibles al primer torn, de 18:00h a 22:30h",
                            type=int)

        parser.add_argument("-p",
                            "--passatgers",
                            help="Defineix el num de passatgers",
                            type=int)

        parser.add_argument("-t",
                            "--traza",
                            help="Defineix si es vol que s'imprimeixi traza. Sí o No.",
                            type=str)

        parser.add_argument("-c",
                            "--csv",
                            help="Defineix si es vol que es generi csv. Sí o No.",
                            type=str)

    def configurarModel(self):
        global mostradors, treballadors, passatgers

        args = parser.parse_args()
        if args.mostrador1:
            ConfigDades.mostradors = args.mostrador1
            ConfigDades.mostradors1 = args.mostrador1
            ConfigDades.mostradors2 = args.mostrador2
            ConfigDades.mostradors3 = args.mostrador3

            ConfigDades.passatgers = args.passatgers
            if(args.traza == "Si"):
                ConfigDades.veuretraza = "Sí"
            if(args.csv == "Si"):
                ConfigDades.csv = "Sí"

        else:
            print("# Comença la configuració")
            ConfigDades.mostradors1 = input(
                f"Quants treballadors vols disponibles al primer torn? - 02:00 - 12:00\n")
            ConfigDades.mostradors2 = input(
                f"Quants treballadors vols disponibles al segon torn? - 12:00 - 18:00\n")
            ConfigDades.mostradors3 = input(
                f"Quants treballadors vols disponibles al tercer torn? - 18:00 - 22:30\n")

            ConfigDades.passatgers = input(f"Quants passatgers? ")
            ConfigDades.veuretraza = input(f"Vols veure traza? Sí, No ")
            ConfigDades.csv = input(
                f"Vols exportar el resultat a csv? Sí, No ")
            print("\n")
