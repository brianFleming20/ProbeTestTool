'''
Created on 3 May 2017
@author: jackw
@amended by Brian F
Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function
Dependencies
-NI VISA Backend
-Non standard python modules
    pyvisa
    pyserial
to do:
-complete button on TPW doesn't work
-TPW freezes if a probe is inserted
-add SQ probe to list
#         s = ttk.Separator(self.root, orient=VERTICAL)
#         s.grid(row=0, column=1, sticky=(N,S))
'''

import Datastore
from tkinter import *
from tkinter import ttk

_TITLE = "This is the title"
PTT_Version = 'self.canvasboard By Danish'  # title Name
GREEN = "#9bdeac"
FONT_NAME = "Courier"
DS = Datastore.Data_Store()


# showing all data in display

class Keyboard():
    def __init__(self):
        self.name_text = None
        self.canvas = None
        self.shift_lock = None
        self.keys = ""

    # First Line Button
    def get_keyboard(self):
        # self.keystrokes = StringVar()
        self.shift_lock = False
        self.canvas = Canvas(width=1100, height=240)

        # Numbers section
        self.name_text = self.canvas.create_text(70, 20, text="lower case", fill="black", font=(FONT_NAME, 12, "bold"))
        one = Button(self.canvas, text='1', width=7, font=("Arial", 12), command=lambda: self.press('1'))
        one.place(relx=0.08, rely=0.17, anchor=CENTER)

        two = Button(self.canvas, text='2', width=7, font=('Arial', 12), command=lambda: self.press('2'))
        two.place(relx=0.16, rely=0.17, anchor=CENTER)

        three = Button(self.canvas, text='3', width=7, font=('Arial', 12), command=lambda: self.press('3'))
        three.place(relx=0.25, rely=0.17, anchor=CENTER)

        four = Button(self.canvas, text='4', width=7, font=('Arial', 12), command=lambda: self.press('4'))
        four.place(relx=0.34, rely=0.17, anchor=CENTER)

        five = Button(self.canvas, text='5', width=7, font=('Arial', 12), command=lambda: self.press('5'))
        five.place(relx=0.43, rely=0.17, anchor=CENTER)

        six = Button(self.canvas, text='6', width=7, font=('Arial', 12), command=lambda: self.press('6'))
        six.place(relx=0.52, rely=0.17, anchor=CENTER)

        seven = Button(self.canvas, text='7', width=7, font=('Arial', 12), command=lambda: self.press('7'))
        seven.place(relx=0.61, rely=0.17, anchor=CENTER)

        eight = Button(self.canvas, text='8', width=7, font=('Arial', 12), command=lambda: self.press('8'))
        eight.place(relx=0.7, rely=0.17, anchor=CENTER)

        nine = Button(self.canvas, text='9', width=7, font=('Arial', 12), command=lambda: self.press('9'))
        nine.place(relx=0.78, rely=0.17, anchor=CENTER)

        zero = Button(self.canvas, text='0', width=7, font=('Arial', 12), command=lambda: self.press('0'))
        zero.place(relx=0.86, rely=0.17, anchor=CENTER)

        clear = Button(self.canvas, text='Clear', width=12, command=self.clear)
        clear.place(relx=0.95, rely=0.17, anchor=CENTER)

        # Frist letter row
        q = Button(self.canvas, text='Q', width=7, font=('Arial', 12), command=lambda: self.press('q'))
        q.place(relx=0.1, rely=0.34, anchor=CENTER)

        w = Button(self.canvas, text='W', width=7, font=('Arial', 12), command=lambda: self.press('w'))
        w.place(relx=0.18, rely=0.34, anchor=CENTER)

        e = Button(self.canvas, text='E', width=7, font=('Arial', 12), command=lambda: self.press('e'))
        e.place(relx=0.26, rely=0.34, anchor=CENTER)

        R = Button(self.canvas, text='R', width=7, font=('Arial', 12), command=lambda: self.press('r'))
        R.place(relx=0.34, rely=0.34, anchor=CENTER)

        T = Button(self.canvas, text='T', width=7, font=('Arial', 12), command=lambda: self.press('t'))
        T.place(relx=0.42, rely=0.34, anchor=CENTER)

        Y = Button(self.canvas, text='Y', width=7, font=('Arial', 12), command=lambda: self.press('y'))
        Y.place(relx=0.5, rely=0.34, anchor=CENTER)

        U = Button(self.canvas, text='U', width=7, font=('Arial', 12), command=lambda: self.press('u'))
        U.place(relx=0.58, rely=0.34, anchor=CENTER)

        I = Button(self.canvas, text='I', width=7, font=('Arial', 12), command=lambda: self.press('i'))
        I.place(relx=0.66, rely=0.34, anchor=CENTER)

        O = Button(self.canvas, text='O', width=7, font=('Arial', 12), command=lambda: self.press('o'))
        O.place(relx=0.74, rely=0.34, anchor=CENTER)

        P = Button(self.canvas, text='P', width=7, font=('Arial', 12), command=lambda: self.press('p'))
        P.place(relx=0.82, rely=0.34, anchor=CENTER)

        # Second Letter Line

        A = Button(self.canvas, text='A', width=7, font=("Courier", 14), command=lambda: self.press('a'))
        A.place(relx=0.12, rely=0.5, anchor=CENTER)

        S = Button(self.canvas, text='S', width=7, font=('Arial', 12), command=lambda: self.press('s'))
        S.place(relx=0.2, rely=0.5, anchor=CENTER)

        D = Button(self.canvas, text='D', width=7, font=('Arial', 12), command=lambda: self.press('d'))
        D.place(relx=0.28, rely=0.5, anchor=CENTER)

        F = Button(self.canvas, text='F', width=7, font=('Arial', 12), command=lambda: self.press('f'))
        F.place(relx=0.36, rely=0.5, anchor=CENTER)

        G = Button(self.canvas, text='G', width=7, font=('Arial', 12), command=lambda: self.press('g'))
        G.place(relx=0.42, rely=0.5, anchor=CENTER)

        H = Button(self.canvas, text='H', width=7, font=('Arial', 12), command=lambda: self.press('h'))
        H.place(relx=0.5, rely=0.5, anchor=CENTER)

        J = Button(self.canvas, text='J', width=7, font=('Arial', 12), command=lambda: self.press('J'))
        J.place(relx=0.58, rely=0.5, anchor=CENTER)

        K = Button(self.canvas, text='K', width=7, font=('Arial', 12), command=lambda: self.press('k'))
        K.place(relx=0.64, rely=0.5, anchor=CENTER)

        L = Button(self.canvas, text='L', width=7, font=('Arial', 12), command=lambda: self.press('l'))
        L.place(relx=0.72, rely=0.5, anchor=CENTER)

        semi_co = Button(self.canvas, text='@', width=7, font=('Arial', 12), command=lambda: self.press('@'))
        semi_co.place(relx=0.8, rely=0.5, anchor=CENTER)

        enter = Button(self.canvas, text='Enter', width=16, font=("Courier", 12),
                           command=lambda check='+': [self.end_keyboard(check), self.canvas.destroy()])
        enter.place(relx=0.92, rely=0.5, anchor=CENTER)

        # third line Button

        shift = Button(self.canvas, text='Shift Lock', width=10, font=('Arial', 12), command=lambda: self.shift())
        shift.place(relx=0.14, rely=0.65, anchor=CENTER)

        Z = Button(self.canvas, text='Z',width=7, font=('Arial', 12), command=lambda: self.press('z'))
        Z.place(relx=0.22, rely=0.65, anchor=CENTER)

        X = Button(self.canvas, text='X', width=7, font=('Arial', 12), command=lambda: self.press('x'))
        X.place(relx=0.3, rely=0.65, anchor=CENTER)

        C = Button(self.canvas, text='C', width=7, font=('Arial', 12), command=lambda: self.press('c'))
        C.place(relx=0.38, rely=0.65, anchor=CENTER)

        V = Button(self.canvas, text='V', width=7, font=('Arial', 12), command=lambda: self.press('v'))
        V.place(relx=0.46, rely=0.65, anchor=CENTER)

        B = Button(self.canvas, text='B', width=7, font=('Arial', 12), command=lambda: self.press('b'))
        B.place(relx=0.52, rely=0.65, anchor=CENTER)

        N = Button(self.canvas, text='N', width=7, font=('Arial', 12), command=lambda: self.press('n'))
        N.place(relx=0.6, rely=0.65, anchor=CENTER)

        M = Button(self.canvas, text='M', width=7, font=('Arial', 12), command=lambda: self.press('m'))
        M.place(relx=0.68, rely=0.65, anchor=CENTER)

        slas = Button(self.canvas, text='/', width=7, font=('Arial', 12), command=lambda: self.press('/'))
        slas.place(relx=0.76, rely=0.65, anchor=CENTER)

        q_mark = Button(self.canvas, text='?', width=7, font=('Arial', 12), command=lambda: self.press('?'))
        q_mark.place(relx=0.84, rely=0.65, anchor=CENTER)

        coma = Button(self.canvas, text='.', width=7, font=('Arial', 12), command=lambda: self.press('.'))
        coma.place(relx=0.92, rely=0.65, anchor=CENTER)

        # Fourth Line Button

        space = Button(self.canvas, text='Space', width=40, command=lambda: self.press(' '))
        space.place(relx=0.5, rely=0.88, anchor=CENTER)

        self.canvas.pack()

    def end_keyboard(self, end):
        self.keys = self.keys + str(end)
        DS.write_to_from_keys(self.keys)
        self.keys = ""

    def display(self):
        self.get_keyboard()

    def clear(self):
        if len(self.keys) == 0:
            self.keys = " "
        self.keys = self.keys[:-1]
        DS.write_to_from_keys(self.keys)

    def action(self):
        DS.write_to_from_keys(self.keys)

    def shift(self):
        if not self.shift_lock:
            self.shift_lock = True
            self.canvas.itemconfig(self.name_text, text="UPPER CASE")
        else:
            self.shift_lock = False
            self.canvas.itemconfig(self.name_text, text="lower case")

    def press(self, num):
        if not self.shift_lock:
            self.keys = self.keys + str(num)

        else:
            cap = str(num).upper()
            self.keys = self.keys + cap

        DS.write_to_from_keys(self.keys)
        # self.keystrokes.set(self.keys)
        # every keyboard press chould be recoreded in the datastore for use in the system.
