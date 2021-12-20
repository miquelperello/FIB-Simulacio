from tkinter import *
from tkinter import messagebox
from Mostradors import *
from datetime import *
from tkinter import ttk


class Config:
    mostradors = "None"
    mostradors1 = "None"
    mostradors2 = "None"
    mostradors3 = "None"
    treballadors = "None"
    passatgers = "None"
    veuretraza = "None"

    def __init__(self):
        self.state = "inactiu"

    def get_mostradors1():
        mostradors1 = ENTRY2.get()
        Config.mostradors1 = mostradors1
        Config.mostradors = mostradors1

    def get_mostradors2():
        mostradors2 = ENTRY3.get()
        Config.mostradors2 = mostradors2

    def get_mostradors3():
        mostradors3 = ENTRY4.get()
        Config.mostradors3 = mostradors3

    def get_passatgers():
        passatgers = ENTRY5.get()
        Config.passatgers = passatgers

    def get_veuretraza():
        veuretraza = comboExample.get()
        if (veuretraza == "Sí"):
            Config.veuretraza = 1
        elif (veuretraza == "No"):
            Config.veuretraza = 0
        else:
            messagebox.showinfo("Result", "Please enter valid data!")

    def get_all():
        Config.get_mostradors1()
        Config.get_mostradors2()
        Config.get_mostradors3()
        Config.get_passatgers()
        Config.get_veuretraza()
        TOP.destroy()

    def configurarModel(self):
        global mostradors, treballadors, passatgers, ENTRY2, ENTRY3, ENTRY4, ENTRY5, TOP, comboExample
        TOP = Tk()
        TOP.geometry("600x500")
        TOP.configure(background="#382343")
        TOP.title("Simulador de Mida")
        TOP.resizable(width=True, height=True)
        bg = PhotoImage(file="airplane.gif")

        # the following alters the Listbox

        ebg = '#382343'
        fg = "#ffffff"
        TOP.option_add('*TCombobox*Listbox*Background', ebg)
        TOP.option_add('*TCombobox*Listbox*Foreground', fg)
        TOP.option_add('*TCombobox*Listbox*selectBackground', fg)
        TOP.option_add('*TCombobox*Listbox*selectForeground', ebg)

        my_canvas = Canvas(TOP)
        my_canvas.pack(fill="both", expand=True)
        my_canvas.create_image(300, 250, image=bg)
        LABEL = Label(TOP, bg="#382343", fg="#ffffff", text="Benvingut a la facturació de la maleta", font=(
            "Helvetica", 15, "bold"), pady=10)
        LABEL.place(x=75, y=0)

        LABEL2 = Label(TOP, bg="#382343", fg="#ffffff", text="Quants treballadors vols disponibles al primer torn? \n 02:00 - 12:00 ",
                       bd=6, font=("Helvetica", 10, "bold"), pady=5)
        LABEL2.place(x=75, y=61)
        ENTRY2 = Entry(TOP, bd=8, width=10, font="Roboto 11")
        ENTRY2.place(x=425, y=61)

        LABEL3 = Label(TOP, bg="#382343", fg="#ffffff", text="Quants treballadors vols disponibles al segon torn? \n 12:00 - 18:00 ",
                       bd=6, font=("Helvetica", 10, "bold"), pady=5)
        LABEL3.place(x=75, y=121)
        ENTRY3 = Entry(TOP, bd=8, width=10, font="Roboto 11")
        ENTRY3.place(x=425, y=121)

        LABEL4 = Label(TOP, bg="#382343", fg="#ffffff", text="Quants treballadors vols disponibles al tercer torn? \n 18:00 - 22:30 ",
                       bd=6, font=("Helvetica", 10, "bold"), pady=5)
        LABEL4.place(x=75, y=181)
        ENTRY4 = Entry(TOP, bd=8, width=10, font="Roboto 11")
        ENTRY4.place(x=425, y=181)

        LABEL5 = Label(TOP, bg="#382343", fg="#ffffff", text="Quants passatgers? ", bd=6, font=(
            "Helvetica", 10, "bold"), pady=5)
        LABEL5.place(x=75, y=241)
        ENTRY5 = Entry(TOP, bd=8, width=10, font="Roboto 11")
        ENTRY5.place(x=425, y=241)

        LABEL6 = Label(TOP, bg="#382343", fg="#ffffff", text="Vols veure traza? 1 Sí, 0 No ", bd=6, font=(
            "Helvetica", 10, "bold"), pady=5)
        LABEL6.place(x=75, y=301)
        ENTRY6 = Entry(TOP, bd=8, width=10, font="Roboto 11")
        #ENTRY6.place(x=425, y=301)

        comboExample = ttk.Combobox(TOP,
                                    values=[
                                        "Sí",
                                        "No",
                                    ])

        comboExample.place(x=360, y=301)

        BUTTON = Button(bg="#382343", fg='#ffffff', bd=12, text="Començar",
                        command=Config.get_all, padx=33, pady=10, font=("Helvetica", 20, "bold"))
        #BUTTON.grid(row=5, column=0, sticky=W)
        BUTTON.place(x=75, y=400)
        TOP.mainloop()
        Config.mostradors = Config.mostradors1
        try:
            #Config.treballadors = Config.get_treballadors()
            #Config.passatgers = str(Config.get_passatgers)
            #Config.veuretraza = str(Config.get_veuretraza)
            a = 2
        except ValueError:
            messagebox.showinfo("Result", "Please enter valid data!")
        print("\n")


# Resultats passatger:  11641   34081   35111
