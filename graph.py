import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("export.csv", sep=",")
llistaComparativa = [df.PerdAvio, df.TempsCua,
                     df.TempsMostrador, df.TempsCuaSortida]
NomComparativa = ['Passatgers que perden avió', 'Temps en fer la cua',
                  'Temps al mostrador', 'Temps desde que entren a la cua fins la sortida']


for item in range(0, len(llistaComparativa)):

    plt.scatter(x=df.Passatgers, y=llistaComparativa[item])

    plt.ylabel(NomComparativa[item])
    plt.xlabel("Passatgers")

    plt.show()
