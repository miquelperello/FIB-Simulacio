from random import randint

class Passatger:
    id = ""
    maleta=""
    documentacio=""
    temps=""

    def __init__(self, temps=None):
        
        
        if (temps == None):
            self.id=randint(0, 1000)
            self.maleta=randint(0, 4)
            self.documentacio=randint(0, 1)
            self.temps = 0
        else:
            self.id=randint(0, 1000)
            self.maleta=randint(0, 4)
            self.documentacio=randint(0, 1)
            self.temps = str(temps)
