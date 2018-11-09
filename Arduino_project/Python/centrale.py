from tkinter import *
import serial
import time
import threading

class Mainmenu(Frame):
    def createWidgets(self):
        self.Afsluiten = Button(self, relief=GROOVE)
        self.Afsluiten["text"] = "Afsluiten"
        self.Afsluiten["command"] = self.quit
        #self.Afsluiten.pack(side=LEFT)
        
        self.nav_control = Button(self, relief=GROOVE)
        self.nav_control["text"] = "Naar control"
        self.nav_control["command"] = self.goto_control
        #self.nav_control.pack(side=RIGHT)

        self.nav_graph = Button(self, relief=GROOVE)
        self.nav_graph["text"] = "Naar grafieken"
        self.nav_graph["command"] = self.goto_grafiek
        #self.nav_graph.pack(side=BOTTOM)

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
        Frame._init_(self, master, width=500, height=300, relief=RAISED)
        self.pack()
        self.createWidgets()
        
#************************

class Controlpanel(Frame):
    def createWidgets(self):
        self.terug = Button(self, relief=GROOVE)
        self.terug["text"] = "Terug naar menu"
        self.terug["command"] = self.quit
        self.terug.grid(row=0, column=0, sticky=W, padx=2, pady=2)

        self.up = Button(self, relief=GROOVE)
        self.up["text"] = "Naar boven"
        self.up["command"] = self.go_up
        self.up.grid(row=1, column=0, sticky=W, padx=2, pady=2)

        self.down = Button(self, relief=GROOVE)
        self.down["text"] = "Naar beneden"
        self.down["command"] = self.go_down
        self.down.grid(row=1, column=2, sticky=W, padx=2, pady=2)

        self.label1 = Label(self, text ="")
        self.label1.grid(row=2)

        self.label = Label(self, text="Voorkeuren voor lichtwaarde:")
        self.label.grid(row=3, columnspan=2,pady=2)

        self.send_input = Button(self, relief=GROOVE)
        self.send_input["text"] = "Verstuur"
        self.send_input["command"] = self.send
        self.send_input.grid(row=4, column=1, sticky=W, padx=2, pady=2)

        self.voorkeur = StringVar(self)
        self.voorkeur.set("3")
        
        self.optie = OptionMenu(self, self.voorkeur, "0", "1", "2", "3")
        self.optie.grid(row=4, column=0, sticky=W, padx=2, pady=2)

    def send(self):
        entry = (self.voorkeur.get())
        try:
            entry = int(entry)
            if(entry == 0):
                ser.write(b'w')
            elif(entry == 1):
                ser.write(b'x')
            elif(entry == 2):
                ser.write(b'y')
            elif(entry == 3):
                ser.write(b'z')
        except:
            print("NO")        

    def go_up(self):
        ser.write(b'o')

    def go_down(self):
        ser.write(b'd')

    def _init_(self, master=None):
        Frame._init_(self, master, width=500, height=300)
        self.pack(side=LEFT)
        self.createWidgets()

#************************

class Grafieken(Frame):
    def createWidgets(self):
        self.terug = Button(self, relief=GROOVE)
        self.terug["text"] = "Terug naar menu"
        self.terug["command"] = self.stop
        self.terug.grid(row=0, column=0, sticky=W, padx=2, pady=2)

        self.draw_can = Button(self, relief=GROOVE)
        self.draw_can["text"] = "Start Grafieken"
        self.draw_can["command"] = self.read_serial_data
        self.draw_can.grid(row=1, column=0, sticky=W, padx=2, pady=2)

        self.stop_can = Button(self, relief=GROOVE)
        self.stop_can["text"] = "Stop Grafieken"
        self.stop_can["command"] = self.stop_check
        self.stop_can.grid(row=1, column=1, sticky=W, padx=2, pady=2)

        self.show_history = Button(self, relief=GROOVE)
        self.show_history["text"] = "Toon geschiedenis"
        self.show_history["command"] = self.history
        self.show_history.grid(row=2, column=0, sticky=W, padx=2, pady=2)

    def maak_canvas(self):
        self.lichtcanvas = Canvas(self.master, width=320, height=400)
        self.tempcanvas = Canvas(self.master, width=320, height=400)

        self.lichtcanvas.pack(side=RIGHT, padx=5)
        self.tempcanvas.pack(side=RIGHT, padx=5)

    def read_serial_data(self):
        self.t = threading.Timer(6.0, self.read_serial_data)
        self.t.start()

        try:
            self.error.destroy()
        except:
            pass
        
        try:
            test = ser.read(1)
            print(test)
            if(test == b'x'):        
                read = ser.read(4)
                read = str(int(read))
                print(read)
                     
                case = int(read[:1])
                temperatuur = int(read[1:])

                self.teken_licht(case, self.counter)
                self.teken_temp(temperatuur, self.counter)

                if(self.counter > 9):
                    self.counter = 0
                    self.lichtcanvas.delete("all")
                    self.tempcanvas.delete("all")
                    self.teken_licht(case, self.counter)
                    self.teken_temp(temperatuur, self.counter)
                    self.counter += 1
                else:
                    self.counter += 1
        except:
            pass

    def teken_licht(self, case, num):
        self.l_licht.append(case)
        if(case == 0):
            y1 = 400
        elif(case == 1):
            y1 = 300
        elif(case == 2):
            y1 = 200
        elif(case == 3):
            y1 = 100

        self.lichtcanvas.create_rectangle(10+30*num, y1, 40+30*num, 400, fill="grey")
        self.lichtcanvas.create_text(25+30*num, y1+10, text=str(case))

    def teken_temp(self, temperatuur, num):
        y1 = 400-temperatuur
        self.l_temp.append(temperatuur/10)
        if(y1 >= 300):
            kleur = "blue"
        elif(y1 > 100):
            kleur = "green"
        else:
            kleur = "red"
            
        self.tempcanvas.create_rectangle(10+30*num, y1, 40+30*num, 400, fill=kleur)
        self.tempcanvas.create_text(25+30*num, y1+10, text=str(temperatuur/10))

    def stop_check(self):
        try:
            self.t.cancel()
        except:
            self.error = Label(self, text="Start eerst de grafieken")
            self.error.grid(row=1, column=2, columnspan=2, sticky=W, padx=2, pady=2)

    def stop(self):
        self.stop_check()
        self.quit()

    def history(self):
        print(self.l_temp)
        print(self.l_licht)

    def _init_(self, master=None):
        Frame._init_(self, master)
        self.pack(side=LEFT)
        self.createWidgets()
        self.maak_canvas()
        self.l_temp = []
        self.l_licht = []
        self.counter = 0

#************************

ser = serial.Serial('COM6', 19200)
if(ser.is_open):
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
