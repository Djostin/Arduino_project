from tkinter import *
import serial
import time
import threading


class Mainmenu(Frame):
    def createWidgets(self):
        self.Afsluiten = Button(self)
        self.Afsluiten["text"] = "Afsluiten"
        self.Afsluiten["command"] = self.quit
        # self.Afsluiten.pack(side=LEFT)

        self.nav_control = Button(self)
        self.nav_control["text"] = "Naar control"
        self.nav_control["command"] = self.goto_control
        # self.nav_control.pack(side=RIGHT)

        self.nav_graph = Button(self)
        self.nav_graph["text"] = "Naar grafieken"
        self.nav_graph["command"] = self.goto_grafiek
        # self.nav_graph.pack(side=BOTTOM)

        self.Afsluiten.grid(row=0, column=0, sticky=W)
        self.nav_control.grid(row=1, column=0, sticky=W)
        self.nav_graph.grid(row=1, column=1, sticky=W)

    def goto_control(self):
        root = Tk()
        root.geometry("700x500")
        root.configure(background="#4682B4")
        root.title("Controle paneel")
        scherm = Controlpanel(master=root)
        scherm.mainloop()
        root.destroy()

    def goto_grafiek(self):
        root = Tk()
        root.geometry("1000x500")
        root.configure(background="#4682B4")
        root.title("Data visualisatie")
        scherm = Grafieken(master=root)
        scherm.mainloop()
        root.destroy()

    def _init_(self, master=None):
        Frame._init_(self, master, width=500, height=300)
        self.pack()
        self.createWidgets()


# ************************

class Controlpanel(Frame):
    def createWidgets(self):
        self.terug = Button(self)
        self.terug["text"] = "Terug naar menu"
        self.terug["command"] = self.quit
        self.terug.grid(row=0, column=0, sticky=W, padx=2, pady=2)

        self.up = Button(self)
        self.up["text"] = "Naar boven"
        self.up["command"] = self.go_up
        self.up.grid(row=1, column=0, sticky=W, padx=2, pady=2)

        self.down = Button(self)
        self.down["text"] = "Naar beneden"
        self.down["command"] = self.go_down
        self.down.grid(row=1, column=2, sticky=W, padx=2, pady=2)

        self.label1 = Label(self, text="")
        self.label1.grid(row=2)

        self.label = Label(self, text="Voorkeuren voor temperatuur:")
        self.label.grid(row=3, columnspan=2, pady=2)

        self.send_input = Button(self)
        self.send_input["text"] = "Verstuur"
        self.send_input["command"] = self.send
        self.send_input.grid(row=4, column=1, sticky=W, padx=2, pady=2)

        self.input = Entry(self)
        self.input.grid(row=4, column=0, padx=2, pady=2)

    def send(self):
        entry = (self.input.get())
        try:
            entry = int(entry)
            ser.write(b'!')
            ser.write(entry)
        except:
            print("NO")

    def go_up(self):
        ser.write(b'o')
        time.sleep(5)
        ser.write(b's')

    def go_down(self):
        ser.write(b'd')
        time.sleep(5)
        ser.write(b's')

    def _init_(self, master=None):
        Frame._init_(self, master, width=500, height=300)
        self.pack(side=LEFT)
        self.createWidgets()


# ************************

class Grafieken(Frame):
    def createWidgets(self):
        self.terug = Button(self)
        self.terug["text"] = "Terug naar menu"
        self.terug["command"] = self.stop
        self.terug.grid(row=0, column=0, sticky=W, padx=2, pady=2)

        self.temp = Button(self)
        self.temp["text"] = "Kies temp"
        self.temp["command"] = self.read_serial_data
        self.temp.grid(row=1, column=0, sticky=W, padx=2, pady=2)

        self.licht = Button(self)
        self.licht["text"] = "Kies licht"
        self.licht["command"] = self.read_serial_data
        self.licht.grid(row=1, column=1, sticky=W, padx=2, pady=2)

    def maak_canvas(self):
        self.lichtcanvas = Canvas(self.master, width=300, height=400)
        self.tempcanvas = Canvas(self.master, width=300, height=400)

        self.lichtcanvas.pack(side=RIGHT, padx=5)
        self.tempcanvas.pack(side=RIGHT, padx=5)

    def read_serial_data(self):
        self.t = threading.Timer(6.0, self.read_serial_data)
        self.t.start()

        try:
            test = ser.read(1)
            print(test)
            if (test == b'x'):
                read = ser.read(4)
                read = str(int(read))
                print(read)

                case = int(read[:1])
                temperatuur = int(read[1:])

                self.teken_licht(case, self.counter)
                self.teken_temp(temperatuur, self.counter)

                self.counter += 1
        except:
            pass

    def teken_licht(self, case, num):
        if (case == 0):
            y1 = 300
            kleur = "black"
        elif (case == 1):
            y1 = 200
            kleur = "grey"
        elif (case == 2):
            y1 = 100
            kleur = "grey"
        elif (case == 3):
            y1 = 0

        self.lichtcanvas.create_rectangle(10 + 30 * num, y1, 40 + 30 * num, 400, fill=kleur)
        self.lichtcanvas.create_text(10 + 30 * num, y1 - 10, text=str(case))

    def teken_temp(self, temperatuur, num):
        y1 = 400 - temperatuur
        if (y1 > 300):
            kleur = "blue"
        elif (y1 < 300 & y1 > 200):
            kleur = "yellow"
        elif (y1 < 200):
            kleur = "red"

        self.tempcanvas.create_rectangle(10 + 30 * num, y1, 40 + 30 * num, 400, fill=kleur)
        self.tempcanvas.create_text(10 + 30 * num, y1 - 10, text=str(temperatuur / 10))

    def _init_(self, master=None):
        Frame._init_(self, master)
        self.pack(side=LEFT)
        self.createWidgets()
        self.maak_canvas()
        self.counter = 0

    def stop(self):
        try:
            self.t.cancel()
        except:
            pass
        self.quit()


# ************************

ser = serial.Serial('COM6', 19200)
if (ser.is_open):
    pass
else:
    ser.open()

root = Tk()
root.geometry("700x500")
root.configure(background="#4682B4")
root.title("Main menu")
scherm = Mainmenu(master=root)
scherm.mainloop()
ser.close()
root.destroy()