from random import randint

class Passatger:
    id = ""
    maleta=""
    documentacio=""
    temps=""
    mostrador_assignat=""

    def __init__(self, temps=None):
        
        global id 
        if (temps == None):
            self.id = randint(200,80000)
            self.maleta=randint(0, 4)
            self.documentacio=randint(0, 1)
            self.temps = 0
            self.mostrador_assignat=-1
        else:
            self.id=randint(0, 10000)
            self.maleta=randint(0, 4)
            self.documentacio=randint(0, 1)
            self.temps = str(temps)
            self.mostrador_assignat=-1