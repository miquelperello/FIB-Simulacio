

import Scheduler
from tkinter import *
from tkinter import messagebox
from Mostradors import *
from datetime import *

class Config:

    mostradors = "None"
    treballadors = "None"
    passatgers = "None"
    veuretraza = "None"


    def __init__(self):
        self.state="inactiu"
        
    def get_treballadors():
        treballadors = ENTRY1.get()
        Config.treballadors = treballadors
    def get_passatgers():
        passatgers = ENTRY2.get()
        Config.passatgers = passatgers
    def get_veuretraza():
        veuretraza = ENTRY3.get()
        Config.veuretraza = int(veuretraza)

    def get_all():
        Config.get_treballadors()
        Config.get_passatgers()
        Config.get_veuretraza()
        TOP.destroy()

    def configurarModel(self):
        global mostradors, treballadors, passatgers, ENTRY1, ENTRY2, ENTRY3, TOP
        TOP = Tk()
        TOP.geometry("600x500")
        TOP.configure(background="#382343")
        TOP.title("Simulador de Mida")
        TOP.resizable(width=False, height=False)
        bg = PhotoImage(file="airplane.gif")

        my_canvas=Canvas(TOP)
        my_canvas.pack(fill="both", expand=True)
        my_canvas.create_image(300, 250, image=bg)
        LABEL = Label(TOP, bg="#382343",fg="#ffffff", text="Benvingut a la facturació de la maleta", font=("Helvetica", 15, "bold"), pady=10)
        LABEL.place(x=105, y=0)
        LABEL1 = Label(TOP, bg="#382343",fg="#ffffff", text="Quants treballadors vols per mostrador? ", bd=6,font=("Helvetica", 10, "bold"), pady=5)
        LABEL1.place(x=105, y=60)
        ENTRY1 = Entry(TOP, bd=8, width=10, font="Roboto 11")
        ENTRY1.place(x=425, y=60)
        LABEL2 = Label(TOP, bg="#382343",fg="#ffffff", text="Quants passatgers? ", bd=6,font=("Helvetica", 10, "bold"), pady=5)
        LABEL2.place(x=105, y=121)
        ENTRY2 = Entry(TOP, bd=8, width=10, font="Roboto 11")
        ENTRY2.place(x=425, y=121)
        LABEL3 = Label(TOP, bg="#382343",fg="#ffffff", text="Vols veure traza? 1 Sí, 0 No ", bd=6,font=("Helvetica", 10, "bold"), pady=5)
        LABEL3.place(x=105, y=181)
        ENTRY3 = Entry(TOP, bd=8, width=10, font="Roboto 11")
        ENTRY3.place(x=425, y=181)
        BUTTON = Button(bg="#382343",fg='#ffffff', bd=12, text="Començar",command = Config.get_all, padx=33, pady=10,font=("Helvetica", 20, "bold"))
        #BUTTON.grid(row=5, column=0, sticky=W)
        BUTTON.place(x=175, y=250)
        TOP.mainloop()
        Config.mostradors = 20
        try:
            #Config.treballadors = Config.get_treballadors()
            #Config.passatgers = str(Config.get_passatgers)
            #Config.veuretraza = str(Config.get_veuretraza)
            a = 2
        except ValueError:
            messagebox.showinfo("Result", "Please enter valid data!")
        print("\n")
        

####Resultats passatger:  11641   34081   35111



    def returnMostradors(self,tid):
        #Segons el temps retornem el num de Mostradors disponibles
        temps1 = datetime.strptime("01/01/21 10:00", "%d/%m/%y %H:%M")
        temps2 = datetime.strptime("01/01/21 18:00", "%d/%m/%y %H:%M")
        temps3 = datetime.strptime("01/01/21 22:30", "%d/%m/%y %H:%M")

        tempsInicial = datetime.strptime("01/01/21 02:00", "%d/%m/%y %H:%M")
        tempsFinal = tempsInicial + datetime(tid)

        if(((tempsFinal < temps1) or ((tempsFinal > temps2) and (tempsFinal < temps3)))):
            return 6
        return 4


    def printTreballadors(self, num):
        global treballadors
        self.treballadors = num
        print("inside print" + str(self.treballadors))
        return self.treballadors
    
    
    def printMostradors(self):
        global mostradors
        print("inside print" + str(self.mostradors))
        return self.mostradors
